import pytest
import asyncio
from app.config.secretes import secretes
from tests.worker_runner import start_workers, stop_workers

COMPLETED_JOB= 38
FAILED_JOB = 12
TOTAL_JOBS = 50


base_paths = [
    f"{secretes.IMAGE_DIR}/girls.jpg",
    f"{secretes.IMAGE_DIR}/arch.jpeg",
    f"{secretes.IMAGE_DIR}/birds.png",
    f"{secretes.IMAGE_DIR}/fakePath999.jpg",
]

test_paths = [
    str(base_paths[i % len(base_paths)])
    for i in range(TOTAL_JOBS)
]

async def submit_job(client, path):
    response = await client.post(
        "/jobs",
        json={"path": path},
    )

    response.raise_for_status()

    data = response.json()

    return response.json()["id"]

async def get_job_by_id(client, id):
    response = await client.get(
        f"/jobs/{id}"
    )

    response.raise_for_status()

    data = response.json()

    return data

async def wait_for_jobs(client, ids, timeout=60):
    start_time = asyncio.get_running_loop().time()
    while True:
        jobs = await asyncio.gather(
            *(get_job_by_id(client, job_id) for job_id in ids)
        )

        finished = all(
            job["status"] in ("completed", "failed")
            for job in jobs
        )

        if finished:
            return jobs

        elapsed = (
            asyncio.get_running_loop().time()
            - start_time
        )

        if elapsed >= timeout:
            pytest.fail(
                f"Jobs did not finish within {timeout} seconds. "
                f"Current jobs: {jobs}"
            )

        await asyncio.sleep(2)

@pytest.mark.asyncio
async def test_100_jobs_with_workers(client):
     workers = []
     try:
        workers = start_workers()
    
        ids = await asyncio.gather(*(submit_job(client, path) for path in test_paths))
    
        assert len(ids) == TOTAL_JOBS
    
        jobs = await wait_for_jobs(client, ids) # Wait for workers to process jobs

        completed = 0
        failed = 0
        for job in jobs:
            if job["status"] == "completed":
                assert job["status"] == "completed"
                assert job["is_blurry"] in (True, False)
                assert job["sharpness_score"] is not None
                assert job["attempts"] == 1
                completed += 1
            else:
                assert job["status"] == "failed"
                assert job["attempts"] == 1
                failed += 1
    
        assert completed == COMPLETED_JOB
        assert failed == FAILED_JOB
        assert completed + failed == TOTAL_JOBS
    
     finally:
        if workers:
         stop_workers(workers)
