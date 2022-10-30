import pytest
from unittest import mock


@pytest.fixture
def create_mock_coro(monkeypatch):
    def _create_mock_patch_coro(to_patch=None):
        m = mock.Mock()

        async def _coro(*args, **kwargs):
            return m(*args, **kwargs)

        if to_patch:
            monkeypatch.setattr(to_patch, _coro)
        return m, _coro

    return _create_mock_patch_coro
