import sqlite3
from pathlib import Path
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