import asyncio
import os
from datetime import datetime, timezone
from sqlalchemy import select
from app.models.jobs import Job
from app.config.database import SessionLocal
import cv2

def process_job(job, threshold: float = 100.0) -> bool:
    image = cv2.imread(job.path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise FileNotFoundError(
            f"Could not open or find the image: {job.path}"
        )

    sharpness_score = cv2.Laplacian(image, cv2.CV_64F).var()

    job.is_blurry = sharpness_score < threshold

    job.sharpness_score = sharpness_score


async def worker():
    worker_id = os.getpid()

    while True:
        try:

            async with SessionLocal.begin() as session:
                stmt = await session.execute(
                    select(Job)
                    .where(Job.status == "pending")
                    .order_by(Job.id)
                    .with_for_update(
                        skip_locked=True
                    )
                    .limit(1)
                )
                job = stmt.scalar_one_or_none()
            

                if job is None:
                    await asyncio.sleep(5)
                    continue

                job.status = "processing"
                job.attempts += 1
               
                try:
                    process_job(job=job)

                    job.status = "completed"

                except Exception as exc:
                    job.status = "failed"
                    job.failed_reason = str(exc)

        except Exception as exc:
            await asyncio.sleep(1)