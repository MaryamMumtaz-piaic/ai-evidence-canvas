from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from app.models.workspace import Workspace

class WorkspaceCreate(BaseModel):
    name: str
    description: Optional[str] = None

class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    canvas_state: Optional[dict] = None

class WorkspaceResponse(Workspace):
    pass

class WorkspaceListResponse(BaseModel):
    workspaces: List[WorkspaceResponse]
