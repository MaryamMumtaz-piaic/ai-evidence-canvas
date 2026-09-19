import json
import aiofiles
from pathlib import Path
from typing import List, Optional
from app.models.evidence import Evidence

DATA_DIR = Path(__file__).parent.parent.parent / 'data' / 'evidence'
INDEX_FILE = DATA_DIR / 'index.json'

async def _update_index(evidence: Evidence, delete: bool = False):
    index = {}
    if INDEX_FILE.exists():
        async with aiofiles.open(INDEX_FILE, 'r') as f:
            index = json.loads(await f.read())
    
    if delete:
        if evidence.id in index:
            del index[evidence.id]
    else:
        index[evidence.id] = evidence.workspace_id
        
    async with aiofiles.open(INDEX_FILE, 'w') as f:
        await f.write(json.dumps(index))

async def save_evidence(evidence: Evidence):
    async with aiofiles.open(DATA_DIR / f"{evidence.id}.json", 'w') as f:
        await f.write(evidence.model_dump_json())
    await _update_index(evidence)

async def get_evidence(id: str) -> Optional[Evidence]:
    file_path = DATA_DIR / f"{id}.json"
    if not file_path.exists():
        return None
    async with aiofiles.open(file_path, 'r') as f:
        data = await f.read()
        return Evidence.model_validate_json(data)

async def list_evidence(workspace_id: str) -> List[Evidence]:
    evidence_list = []
    index = {}
    if INDEX_FILE.exists():
        async with aiofiles.open(INDEX_FILE, 'r') as f:
            index = json.loads(await f.read())
            
    for eid, wid in index.items():
        if wid == workspace_id:
            ev = await get_evidence(eid)
            if ev:
                evidence_list.append(ev)
    return evidence_list

async def delete_evidence(id: str):
    file_path = DATA_DIR / f"{id}.json"
    if file_path.exists():
        ev = await get_evidence(id)
        file_path.unlink()
        if ev:
            await _update_index(ev, delete=True)

async def update_evidence(evidence: Evidence):
    await save_evidence(evidence)
