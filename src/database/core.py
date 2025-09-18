from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from collections.abc import AsyncGenerator

import os
from dotenv import load_dotenv

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(DATABASE_URL)

async_session_meker = async_sessionmaker(async_engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_session()-> AsyncGenerator[AsyncSession, None]:
    async with async_session_meker() as session:
        yield session

session_dep = Annotated[AsyncSession, Depends(get_async_session)]