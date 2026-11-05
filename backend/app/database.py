# import os
# from dotenv import load_dotenv
# from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
# from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
# from typing import AsyncGenerator

# load_dotenv()

# #Postgresql URL
# DATABASE_URL = os.getenv("DATABASE_URL")

# #Create async engine
# engine = create_async_engine(DATABASE_URL, echo=True)

# #Create async sessionmaker
# AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession,expire_on_commit=False)

# #Base class for sqlalchemy models
# class Base(DeclarativeBase):
#     pass

# #Dependency to get DB session in fastapi routes
# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         yield session

import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

load_dotenv()

# Fetching raw database url from Render environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif not DATABASE_URL:
    # Local fallback address agar .env absent ho
    DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/devtracker"

# Create async engine with explicit dialect driver
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async sessionmaker
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base class for sqlalchemy models
class Base(DeclarativeBase):
    pass

# Dependency to get DB session in fastapi routes
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
