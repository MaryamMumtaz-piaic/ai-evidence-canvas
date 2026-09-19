from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Workspace(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    evidence_count: int = 0
    relationship_count: int = 0
    canvas_state: dict = {}
    tags: List[str] = []
