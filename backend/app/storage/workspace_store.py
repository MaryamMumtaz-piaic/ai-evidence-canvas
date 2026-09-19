import json
import aiofiles
from pathlib import Path
from typing import List, Optional
from app.models.workspace import Workspace

DATA_DIR = Path(__file__).parent.parent.parent / 'data' / 'workspaces'

async def save_workspace(workspace: Workspace):
    async with aiofiles.open(DATA_DIR / f"{workspace.id}.json", 'w') as f:
        await f.write(workspace.model_dump_json())

async def get_workspace(id: str) -> Optional[Workspace]:
    file_path = DATA_DIR / f"{id}.json"
    if not file_path.exists():
        return None
    async with aiofiles.open(file_path, 'r') as f:
        data = await f.read()
        return Workspace.model_validate_json(data)

async def list_workspaces() -> List[Workspace]:
    workspaces = []
    for file_path in DATA_DIR.glob('*.json'):
        async with aiofiles.open(file_path, 'r') as f:
            data = await f.read()
            workspaces.append(Workspace.model_validate_json(data))
    return workspaces

async def delete_workspace(id: str):
    file_path = DATA_DIR / f"{id}.json"
    if file_path.exists():
        file_path.unlink()

async def update_workspace(workspace: Workspace):
    await save_workspace(workspace)
