import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from pathlib import Path
import tempfile
import shutil

@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def tmp_data_dir(tmp_path, monkeypatch):
    # Override data directory to temp path for tests
    for d in ['workspaces', 'evidence', 'embeddings', 'relationships']:
        (tmp_path / d).mkdir()
    return tmp_path

@pytest.fixture
async def client(tmp_data_dir):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac
