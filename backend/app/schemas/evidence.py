from pydantic import BaseModel
from typing import Optional, List
from app.models.evidence import Evidence

class EvidenceNoteCreate(BaseModel):
    workspace_id: str
    title: str
    content: str

class EvidenceURLCreate(BaseModel):
    workspace_id: str
    url: str
    title: str

class EvidenceResponse(Evidence):
    pass

class EvidenceListResponse(BaseModel):
    evidence: List[EvidenceResponse]

class CanvasPositionUpdate(BaseModel):
    x: float
    y: float
    width: float
    height: float
