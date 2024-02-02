from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import (
    PG_DB,
    PG_HOST,
    PG_USER,
    PG_PASSWORD,
    PG_PORT,
)


engine = create_async_engine(
    f'postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
)
Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
