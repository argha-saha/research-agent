from typing import Optional, List, Dict, Any
from sessions.database import ResearchDatabase
from models.research_response import ResearchResponse


class SessionManager:
    def __init__(self, db_path: str = "research_sessions.db"):
        self.db = ResearchDatabase(db_path)
        self.current_session_id: Optional[int] = None
        self.current_session_data: Optional[Dict[str, Any]] = None

    def create_new_session(
        self, topic: str, model_used: str, metadata: Dict[str, Any] = None
    ) -> int:
        session_id = self.db.create_session(topic, model_used, metadata)
        self.current_session_id = session_id
        self.current_session_data = self.db.get_session(session_id)
        return session_id

    def load_session(self, session_id: int) -> bool:
        session_data = self.db.get_session(session_id)
        if session_data:
            self.current_session_id = session_id
            self.current_session_data = session_data
            return True

        return False

    def get_current_session(self) -> Optional[Dict[str, Any]]:
        return self.current_session_data

    def get_current_session_entries(self) -> List[Dict[str, Any]]:
        if self.current_session_id:
            return self.db.get_session_entries(self.current_session_id)
        
        return []
