from dotenv import load_dotenv
import pathlib
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from collections.abc import AsyncGenerator


path = pathlib.Path(__file__).parent
load_dotenv(str(path) + '/.env')


username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DB_NAME')


engine = create_async_engine(f'postgresql+asyncpg://{username}:{password}'
                       f'@{host}/{database}',  pool_pre_ping=True,echo=True)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator:
    async with async_session_maker() as db:
        try:
            yield db
        finally:
            await db.close()
