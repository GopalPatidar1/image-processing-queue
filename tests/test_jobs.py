import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from worker.main import start_job
 
@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_get_jobs(client):
    response = await client.get("/jobs")
    response_json = response.json()

    assert response.status_code == 200
    assert "avail_next" in response_json
    assert "next_cursor" in response_json
    assert "result" in response_json

@pytest.mark.asyncio
async def test_get_by_id(client):
    response = await client.get("/jobs/99999")
    response_json = response.json()
    assert response.status_code == 404
    assert response_json["error"] == 'jobs not found'

@pytest.mark.asyncio
async def test_create_job(client):
    response = await client.post("/jobs", json={
        'path': '/home/sitaram/Documents/project/practice_projection/image/girls.jpg'
    })
    response_json = response.json()
    assert response.status_code == 201
    assert "id" in response_json

@pytest.mark.asyncio
async def test_create_job_wrong_body(client):
    response = await client.post("/jobs", json={
        'path1': '/home/sitaram/Documents/project/practice_projection/image/girls.jpg'
    })
    response_json = response.json()
    assert response.status_code == 422
    assert "id" not in response_json


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'path, expected_status',
    [
        (
            '/home/sitaram/Documents/project/practice_projection/image/girls.jpg',
            'completed'
        ),
        (
            '/home/sitaram/Documents/project/practice_projection/image/fakePath.jpg',
            'failed'
        )
    ]
)
async def test_worker_processes_job(client, path, expected_status):
    response = await client.post("/jobs", json={"path": path})
    response_json = response.json()

    assert "id" in response_json
    
    job = await start_job(response_json['id'])
    assert job.status == expected_status