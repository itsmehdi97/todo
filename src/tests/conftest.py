import pytest
import pytest_asyncio

from core.config import get_settings
from adapters import orm
from db.tasks import connect_to_db
from services.unit_of_work import SqlAlchemyUnitOfWork


settings = get_settings()


@pytest_asyncio.fixture
async def memory_session_factory():
    session, engine = await connect_to_db(url="sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(orm.mapper_registry.metadata.drop_all)
        await conn.run_sync(orm.mapper_registry.metadata.create_all)

    yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def session_factory():
    session, engine = await connect_to_db(url=settings.DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(orm.mapper_registry.metadata.drop_all)
        await conn.run_sync(orm.mapper_registry.metadata.create_all)

    yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def in_memory_db(memory_session_factory):
    session = memory_session_factory()
    yield session
    await session.close()


@pytest_asyncio.fixture
async def db(session_factory):
    session = session_factory()
    yield session
    await session.close()


@pytest.fixture
def uow(memory_session_factory):
    return SqlAlchemyUnitOfWork(memory_session_factory)
