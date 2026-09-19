import pytest

@pytest.mark.asyncio
async def test_create_workspace(client):
    response = await client.post("/api/workspaces", json={"name": "Test Workspace", "description": "Test Desc"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Workspace"

@pytest.mark.asyncio
async def test_create_workspace_missing_name(client):
    response = await client.post("/api/workspaces", json={"description": "Missing name"})
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_workspaces(client):
    # First create one
    await client.post("/api/workspaces", json={"name": "List Test", "description": "Desc"})
    response = await client.get("/api/workspaces")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

@pytest.mark.asyncio
async def test_get_workspace(client):
    create_resp = await client.post("/api/workspaces", json={"name": "Get Test"})
    ws_id = create_resp.json()["id"]
    response = await client.get(f"/api/workspaces/{ws_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ws_id

@pytest.mark.asyncio
async def test_get_nonexistent_workspace(client):
    response = await client.get("/api/workspaces/fake_id_123")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_workspace(client):
    create_resp = await client.post("/api/workspaces", json={"name": "Update Test"})
    ws_id = create_resp.json()["id"]
    response = await client.patch(f"/api/workspaces/{ws_id}", json={"name": "Updated Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

@pytest.mark.asyncio
async def test_delete_workspace(client):
    create_resp = await client.post("/api/workspaces", json={"name": "Delete Test"})
    ws_id = create_resp.json()["id"]
    response = await client.delete(f"/api/workspaces/{ws_id}")
    assert response.status_code == 200
    # Verify deletion
    get_resp = await client.get(f"/api/workspaces/{ws_id}")
    assert get_resp.status_code == 404
