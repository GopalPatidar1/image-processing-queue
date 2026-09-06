from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.jobs import CreateJob, JobGetResponse, JobItems
from app.service import jobs
from app.config.database import get_db
from fastapi import status
from app.models.jobs import StatusEnum

router = APIRouter(prefix="/jobs", tags=[
    'Jobs'
])

@router.get('/', response_model=JobGetResponse)
async def get_jobs(next_cursor: int | None= None, status: StatusEnum | None= None, limit: int = 10, db: AsyncSession = Depends(get_db)):
  return await jobs.get_jobs(db, limit=limit, next_cursor=next_cursor, status=status)

@router.get('/{id}', response_model=JobItems)
async def get_job_by_id(id: int, db: AsyncSession = Depends(get_db)):
  return await jobs.get_job_by_id(db= db, id=id)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_job(data: CreateJob, db: AsyncSession = Depends(get_db)):
  return await jobs.create_job(data= data, db= db)