from pydantic import BaseModel
from typing import List, Optional
from app.models.relationship import Relationship, RelationshipType

class RelationshipCreate(BaseModel):
    source_id: str
    target_id: str
    type: RelationshipType
    confidence: float
    reason: str

class RelationshipResponse(Relationship):
    pass

class RelationshipListResponse(BaseModel):
    relationships: List[RelationshipResponse]
