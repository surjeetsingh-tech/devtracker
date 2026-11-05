import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from typing import AsyncGenerator

load_dotenv()

#Postgresql URL
DATABASE_URL = os.getenv("DATABASE_URL")

#Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

#Create async sessionmaker
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession,expire_on_commit=False)

#Base class for sqlalchemy models
class Base(DeclarativeBase):
    pass

#Dependency to get DB session in fastapi routes
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
