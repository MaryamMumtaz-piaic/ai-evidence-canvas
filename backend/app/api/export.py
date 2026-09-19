from fastapi import APIRouter

router = APIRouter(tags=["Export"])

@router.post("/workspaces/{id}/export")
async def export_workspace(id: str):
    # Stub: same as workspaces export, just a dedicated route
    return {"exported": True}
