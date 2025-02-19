from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite+aiosqlite:///jobs.db"
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# Base para definir modelos
class Base(DeclarativeBase):
    pass


# Modelo de la tabla 'job_listings'
class JobListingDB(Base):
    __tablename__ = "job_listings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    location = Column(String)
    salary = Column(String, nullable=True)
    modality = Column(String, nullable=True)
    link = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)


# Crear la base de datos y las tablas
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def save_jobs_to_db(jobs):
    async with SessionLocal() as session:
        for job in jobs:
            existing_job = await session.execute(
                JobListingDB.__table__.select().where(JobListingDB.link == job["link"])
            )
            if existing_job.scalar_one_or_none() is None:
                new_job = JobListingDB(
                    title=job["title"],
                    company=job["company"],
                    location=job["location"],
                    salary=job["salary"],
                    modality=job["modality"],
                    link=job["link"],
                    description=job["description"],
                )
                session.add(new_job)

        await session.commit()
