from fastapi import APIRouter
from app.schemas.relationship import RelationshipCreate, RelationshipResponse

router = APIRouter(tags=["Relationships"])

@router.get("/relationships/{id}")
async def get_relationship(id: str):
    # Stub
    return {}

@router.post("/relationships")
async def create_relationship(rel: RelationshipCreate):
    # Stub
    return {}

@router.delete("/relationships/{id}")
async def delete_relationship(id: str):
    # Stub
    return {"status": "deleted"}
