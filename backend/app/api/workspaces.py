from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse, WorkspaceListResponse
from app.models.workspace import Workspace
from app.storage import workspace_store
from datetime import datetime
import uuid

router = APIRouter(tags=["Workspaces"])

@router.post("/workspaces", response_model=WorkspaceResponse)
async def create_workspace(workspace_in: WorkspaceCreate):
    workspace = Workspace(
        id=str(uuid.uuid4()),
        name=workspace_in.name,
        description=workspace_in.description,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    await workspace_store.save_workspace(workspace)
    return workspace

@router.get("/workspaces", response_model=WorkspaceListResponse)
async def list_workspaces():
    workspaces = await workspace_store.list_workspaces()
    return {"workspaces": workspaces}

@router.get("/workspaces/{id}", response_model=WorkspaceResponse)
async def get_workspace(id: str):
    workspace = await workspace_store.get_workspace(id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace

@router.patch("/workspaces/{id}", response_model=WorkspaceResponse)
async def update_workspace(id: str, updates: WorkspaceUpdate):
    workspace = await workspace_store.get_workspace(id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    if updates.name is not None:
        workspace.name = updates.name
    if updates.description is not None:
        workspace.description = updates.description
    if updates.canvas_state is not None:
        workspace.canvas_state = updates.canvas_state
        
    workspace.updated_at = datetime.utcnow()
    await workspace_store.update_workspace(workspace)
    return workspace

@router.delete("/workspaces/{id}")
async def delete_workspace(id: str):
    workspace = await workspace_store.get_workspace(id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    await workspace_store.delete_workspace(id)
    return {"status": "deleted"}

@router.get("/workspaces/{id}/relationships")
async def list_workspace_relationships(id: str):
    # Stub: delegate to relationship service or store
    return {"relationships": []}

@router.get("/workspaces/{id}/timeline")
async def get_workspace_timeline(id: str):
    # Stub: timeline events
    return {"timeline": []}

@router.get("/workspaces/{id}/graph")
async def get_workspace_graph(id: str):
    # Stub: nodes and edges
    return {"nodes": [], "edges": []}

@router.post("/workspaces/{id}/analyze", status_code=202)
async def analyze_workspace(id: str, background_tasks: BackgroundTasks):
    # Stub: triggers full relationship analysis
    def background_analyze(workspace_id):
        pass
    background_tasks.add_task(background_analyze, id)
    return {"status": "Analysis started"}

@router.post("/workspaces/{id}/export")
async def export_workspace_investigation(id: str):
    # Stub
    return {"export": "data"}
