import sqlite3
from pathlib import Path
from models.research_response import ResearchResponse


class ResearchDatabase:
    def __init__(self, db_path: str = "research_sessions.db"):
        self.db_path = Path(db_path)
        self._init_database()

    def _init_database(self):
        """Initialize the database with required tables"""
