import pytest
from adapters import orm


@pytest.fixture(autouse=True, scope="session")
def mappers():
    orm.start_mappers()
    yield
    orm.clear_mappers()
