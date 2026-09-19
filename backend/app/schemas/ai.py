from pydantic import BaseModel
from typing import List, Optional
from app.schemas.evidence import EvidenceResponse

class SearchQuery(BaseModel):
    query: str
    workspace_id: str
    limit: int = 5

class AskQuery(BaseModel):
    question: str
    workspace_id: str

class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    confidence: float

class SearchResponse(BaseModel):
    results: List[EvidenceResponse]
