import pytest

@pytest.fixture
async def workspace_id(client):
    resp = await client.post("/api/workspaces", json={"name": "Evidence Test WS"})
    return resp.json()["id"]

@pytest.mark.asyncio
async def test_create_note_evidence(client, workspace_id):
    payload = {
        "workspace_id": workspace_id,
        "type": "note",
        "title": "Test Note",
        "content": "This is a test note."
    }
    response = await client.post("/api/evidence/note", json=payload)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Note"

@pytest.mark.asyncio
async def test_create_note_missing_content(client, workspace_id):
    payload = {
        "workspace_id": workspace_id,
        "type": "note",
        "title": "Missing Content Note"
    }
    response = await client.post("/api/evidence/note", json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_evidence(client, workspace_id):
    await client.post("/api/evidence/note", json={
        "workspace_id": workspace_id, "type": "note", "title": "T1", "content": "C1"
    })
    response = await client.get(f"/api/workspaces/{workspace_id}/evidence")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

@pytest.mark.asyncio
async def test_get_evidence(client, workspace_id):
    create_resp = await client.post("/api/evidence/note", json={
        "workspace_id": workspace_id, "type": "note", "title": "T2", "content": "C2"
    })
    ev_id = create_resp.json()["id"]
    response = await client.get(f"/api/evidence/{ev_id}")
    assert response.status_code == 200
    assert response.json()["id"] == ev_id

@pytest.mark.asyncio
async def test_delete_evidence(client, workspace_id):
    create_resp = await client.post("/api/evidence/note", json={
        "workspace_id": workspace_id, "type": "note", "title": "T3", "content": "C3"
    })
    ev_id = create_resp.json()["id"]
    response = await client.delete(f"/api/evidence/{ev_id}")
    assert response.status_code == 200
    get_resp = await client.get(f"/api/evidence/{ev_id}")
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_update_canvas_position(client, workspace_id):
    create_resp = await client.post("/api/evidence/note", json={
        "workspace_id": workspace_id, "type": "note", "title": "T4", "content": "C4"
    })
    ev_id = create_resp.json()["id"]
    pos = {"x": 100, "y": 200, "width": 300, "height": 400}
    response = await client.patch(f"/api/evidence/{ev_id}", json={"canvas_position": pos})
    assert response.status_code == 200
    assert response.json()["canvas_position"]["x"] == 100

@pytest.mark.asyncio
async def test_url_validation(client, workspace_id):
    payload = {
        "workspace_id": workspace_id,
        "type": "url",
        "title": "Bad URL",
        "source_url": "not_a_valid_url"
    }
    response = await client.post("/api/evidence/url", json=payload)
    # The actual implementation of evidence routes might differ, 
    # but based on requirements we expect 422 for invalid URL evidence payload.
    assert response.status_code == 422
