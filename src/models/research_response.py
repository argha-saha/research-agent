from pydantic import BaseModel

class ResearchResponse(BaseModel):
    topic: str
    result: str
    sources: list[str]
    tools_used: list[str]