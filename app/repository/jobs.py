from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.models.jobs import Job
from sqlalchemy.ext.asyncio import AsyncSession

async def create_jobs(db:AsyncSession, data):
    db.add(data)

async def get_jobs(db: AsyncSession, next_cursor: int | None, limit:int, status: str | None):
    filter_rec = []

    if next_cursor is not None:
        filter_rec.append(Job.id <= next_cursor)

    if status is not None:
        filter_rec.append(Job.status == status)

    result = await db.scalars(
        select(Job)
        .where(*filter_rec)
        .order_by(Job.id.desc())
        .limit(limit+1)
    )

    return result.all()

async def get_job_by_id(db: AsyncSession, id: int | None):
    return await db.scalar(
        select(Job)
        .where(Job.id == id)
    )

async def updateJob(db: AsyncSession, jobId:int, data):
     result = await db.execute(
        update(Job)
        .where(
            Job.id == jobId,
        )
        .values(**data.model_dump(exclude_unset=True))
        .returning(Job)
       )

     await db.commit()

     return result.scalar_one_or_none()