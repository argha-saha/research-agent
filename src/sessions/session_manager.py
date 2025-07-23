from typing import Optional, List, Dict, Any
from sessions.database import ResearchDatabase
from models.research_response import ResearchResponse


class SessionManager:
    def __init__(self, db_path: str = "research_sessions.db"):
        self.db = ResearchDatabase(db_path)
        self.current_session_id: Optional[int] = None
        self.current_session_data: Optional[Dict[str, Any]] = None