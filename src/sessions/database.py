import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from models.research_response import ResearchResponse


class ResearchDatabase:
    def __init__(self, db_path: str = "research_sessions.db"):
        self.db_path = Path(db_path)
        self._init_database()
    
    def _init_database(self):
        """Initialize the database with required tables and indexes"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    topic TEXT NOT NULL,
                    model_used TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    metadata TEXT DEFAULT '{}'
                )
            """)
            
            # Create research_entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS research_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    query TEXT NOT NULL,
                    result TEXT NOT NULL,
                    sources TEXT NOT NULL,
                    tools_used TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            """)
            
            # Create indexes for better query performance
            # Sessions table indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_updated_at 
                ON sessions (updated_at DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_created_at 
                ON sessions (created_at DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_status 
                ON sessions (status)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_sessions_model_used 
                ON sessions (model_used)
            """)
            
            # Research entries table indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_research_entries_session_id 
                ON research_entries (session_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_research_entries_timestamp 
                ON research_entries (timestamp ASC)
            """)
            
            # Composite index (session_id + timestamp)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_research_entries_session_timestamp 
                ON research_entries (session_id, timestamp ASC)
            """)
            
            conn.commit()
    
    def create_session(self, topic: str, model_used: str, metadata: Dict[str, Any] = None) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            metadata_json = json.dumps(metadata or {})
            
            cursor.execute("""
                INSERT INTO sessions (topic, model_used, metadata)
                VALUES (?, ?, ?)
            """, (topic, model_used, metadata_json))
            
            return cursor.lastrowid
    
    def add_research_entry(self, session_id: int, query: str, research_response: ResearchResponse) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO research_entries (session_id, query, result, sources, tools_used)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session_id,
                query,
                research_response.result,
                json.dumps(research_response.sources),
                json.dumps(research_response.tools_used)
            ))
            
            cursor.execute("""
                UPDATE sessions 
                SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (session_id,))
            
            return cursor.lastrowid
    
    def get_session(self, session_id: int) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, topic, model_used, created_at, updated_at, status, metadata
                FROM sessions WHERE id = ?
            """, (session_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'topic': row[1],
                    'model_used': row[2],
                    'created_at': row[3],
                    'updated_at': row[4],
                    'status': row[5],
                    'metadata': json.loads(row[6])
                }
            return None
    
    def get_session_entries(self, session_id: int) -> List[Dict[str, Any]]:
        """Get all research entries for a session"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, query, result, sources, tools_used, timestamp
                FROM research_entries 
                WHERE session_id = ?
                ORDER BY timestamp ASC
            """, (session_id,))
            
            entries = []
            for row in cursor.fetchall():
                entries.append({
                    'id': row[0],
                    'query': row[1],
                    'result': row[2],
                    'sources': json.loads(row[3]),
                    'tools_used': json.loads(row[4]),
                    'timestamp': row[5]
                })
            
            return entries
    
    def list_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """List recent sessions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, topic, model_used, created_at, updated_at, status
                FROM sessions 
                ORDER BY updated_at DESC 
                LIMIT ?
            """, (limit,))
            
            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    'id': row[0],
                    'topic': row[1],
                    'model_used': row[2],
                    'created_at': row[3],
                    'updated_at': row[4],
                    'status': row[5]
                })
            
            return sessions
    
    def delete_session(self, session_id: int) -> bool:
        """Delete a session and all its research entries"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Delete research entries first
            cursor.execute("DELETE FROM research_entries WHERE session_id = ?", (session_id,))
            
            # Delete session
            cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            
            return cursor.rowcount > 0