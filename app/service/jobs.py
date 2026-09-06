from app.repository import jobs 
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.custom_exception import CustomException
from fastapi import status
from app.models.jobs import Job
from app.schema.jobs import CreateJob

async def create_job(data: CreateJob, db: AsyncSession):
    try:
     job_data = Job(
       path=data.path
     )

     await jobs.create_jobs(db=db, data=job_data)

     await db.commit()

     await db.refresh(job_data)
 
     return { "id": job_data.id }

    except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR)

async def get_jobs(db:AsyncSession, limit: int, next_cursor: int | None, **kwargs):
  filter_status = kwargs.get("status", None)
  try:
   result = await jobs.get_jobs(db, next_cursor=next_cursor, limit=limit, status=filter_status)

   next_cursor = result[-1].id if result else None
   avail_next = len(result) > limit
   return { "next_cursor": next_cursor, "avail_next": avail_next, "result": result[:limit] }
  
  except Exception as e:
    await db.rollback()
    raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch jobs")

async def get_job_by_id(db: AsyncSession, id: int):
   try:
     jobs_data =  await jobs.get_job_by_id(db=db, id=id)
     if jobs_data is None:
        raise CustomException(status.HTTP_404_NOT_FOUND, "jobs not found")
     await db.commit()

     return jobs_data
   
   except CustomException:
     raise
   
   except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch job")
