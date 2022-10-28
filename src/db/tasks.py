from asyncio import current_task

from fastapi import FastAPI

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings
from db import Session

import logging


logger = logging.getLogger(__name__)


async def connect_to_db(
    app: FastAPI = None,
    url: str = None,
    expire_on_commit: bool = False
) -> Session:
    url = url or get_settings().DATABASE_URL

    try:
        engine = create_async_engine(url)
        session_factory = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=expire_on_commit)
        AsyncScopedSession = async_scoped_session(
            session_factory, scopefunc=current_task
        )
        if app:
            app.state._db_engine = engine
            app.state._db = AsyncScopedSession
        return AsyncScopedSession, engine

    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db_engine.dispose()

    except Exception as e:
        logger.warning("--- DB DISCONNECT ERROR ---")
        logger.warning(e)
        logger.warning("--- DB DISCONNECT ERROR ---")
