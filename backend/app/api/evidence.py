from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Form
from app.schemas.evidence import EvidenceNoteCreate, EvidenceURLCreate, EvidenceResponse, EvidenceListResponse, CanvasPositionUpdate
from app.models.evidence import Evidence, EvidenceType, ProcessingStatus, EvidenceQuality
from app.storage import evidence_store
from datetime import datetime
import uuid

router = APIRouter(tags=["Evidence"])

@router.get("/workspaces/{id}/evidence", response_model=EvidenceListResponse)
async def list_evidence(id: str):
    evidence_list = await evidence_store.list_evidence(id)
    return {"evidence": evidence_list}

@router.post("/evidence/note", response_model=EvidenceResponse)
async def create_note_evidence(note: EvidenceNoteCreate):
    ev = Evidence(
        id=str(uuid.uuid4()),
        workspace_id=note.workspace_id,
        type=EvidenceType.NOTE,
        title=note.title,
        source_name="Manual Note",
        content=note.content,
        status=ProcessingStatus.READY,
        quality=EvidenceQuality(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    await evidence_store.save_evidence(ev)
    return ev

@router.post("/evidence/url", status_code=202)
async def create_url_evidence(url_req: EvidenceURLCreate, background_tasks: BackgroundTasks):
    ev = Evidence(
        id=str(uuid.uuid4()),
        workspace_id=url_req.workspace_id,
        type=EvidenceType.URL,
        title=url_req.title,
        source_name=url_req.url,
        source_url=url_req.url,
        status=ProcessingStatus.PROCESSING,
        quality=EvidenceQuality(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    await evidence_store.save_evidence(ev)
    
    def process_url(ev_id):
        # Stub
        pass
    background_tasks.add_task(process_url, ev.id)
    return ev

@router.post("/evidence/upload")
async def upload_evidence(
    workspace_id: str = Form(...),
    file: UploadFile = File(...)
):
    # Stub: handle file upload
    return {"status": "uploaded", "filename": file.filename}

@router.get("/evidence/{id}", response_model=EvidenceResponse)
async def get_evidence(id: str):
    ev = await evidence_store.get_evidence(id)
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return ev

@router.patch("/evidence/{id}", response_model=EvidenceResponse)
async def update_evidence_canvas(id: str, position: CanvasPositionUpdate):
    ev = await evidence_store.get_evidence(id)
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence not found")
    ev.canvas_position = position.model_dump()
    ev.updated_at = datetime.utcnow()
    await evidence_store.update_evidence(ev)
    return ev

@router.delete("/evidence/{id}")
async def delete_evidence(id: str):
    await evidence_store.delete_evidence(id)
    return {"status": "deleted"}

@router.get("/evidence/{id}/chunks")
async def get_evidence_chunks(id: str):
    ev = await evidence_store.get_evidence(id)
    if not ev:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return {"chunks": ev.chunks}
