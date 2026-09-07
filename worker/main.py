import asyncio
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, update, and_, or_
from app.models.jobs import Job
from app.config.database import SessionLocal
import cv2

import logging 
from app.core.logger import setup_logger 
setup_logger() 

async def recover_stale_jobs():
    try:
       JOB_TIMEOUT = timedelta(minutes=2)
       cutoff = datetime.now(timezone.utc) - JOB_TIMEOUT
   
       async with SessionLocal.begin() as session:
           stmt = (
               update(Job)
               .where(Job.status == "processing", Job.started_at < cutoff,)
               .values(
                   status="pending",
                   next_attempt_at=datetime.now(timezone.utc),
                   failed_reason="Recovered after worker restart",
               )
           )
           await session.execute(stmt)
    except Exception as exc:
        logging.exception("Failed to recover stale jobs")

def process_job(path, threshold: float = 100.0) -> bool:
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError(
            f"Invalid image or unsupported image format: {path}"
        )

    sharpness_score = cv2.Laplacian(image, cv2.CV_64F).var()

    is_blurry = sharpness_score < threshold

    return is_blurry, sharpness_score


async def start_job(jobId: int | None = None) -> bool:
    now = datetime.now(timezone.utc)

    if jobId is not None:
         filter_condition = Job.id == jobId
    else:
         filter_condition = and_(
             Job.status == "pending",
             or_(
                 Job.next_attempt_at.is_(None),
                 Job.next_attempt_at <= now,
             ),
         )
     
    async with SessionLocal.begin() as session:
         stmt = await session.execute(
             select(Job)
             .where(filter_condition)
             .order_by(Job.id)
             .with_for_update(
                 skip_locked=True
             )
             .limit(1)
         )
         job = stmt.scalar_one_or_none()
     
         if job is None:
             await asyncio.sleep(5)
             return False

         job.status = "processing"
         job.started_at = now
         job.attempts += 1
         job_id = job.id

    try:
         is_blurry, sharpness_score = process_job(job.path)
         job.status = "completed"
    except Exception as exc:
        async with SessionLocal.begin() as session: 
           result = await session.execute( select(Job).where(Job.id == job_id)) 
           job = result.scalar_one_or_none() 
           if job is not None: 
              job.status = "failed" 
              job.failed_reason = str(exc) 
        return False

    async with SessionLocal.begin() as session: 
         result = await session.execute( select(Job).where(Job.id == job_id)) 

         job = result.scalar_one_or_none() 
         if job is not None: 
             job.is_blurry = is_blurry 
             job.sharpness_score = sharpness_score 
             job.status = "completed" 
             return True

async def worker():
    await recover_stale_jobs()
    while True:
        try:
            await start_job()
        except Exception as exc:
            logging.exception("Worker failed")
            await asyncio.sleep(1)