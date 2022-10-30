import pytest
from unittest import mock
from datetime import datetime

import schemas
from adapters.repository import TodoRepository
from services.permissions import DeveloperPermService


@pytest.fixture
def fake_repo():
    mock_session = mock.Mock()
    return TodoRepository(mock_session)


@pytest.mark.asyncio
async def test_memberof_returns_true_when_user_in_project(fake_repo, create_mock_coro):
    mock_user_in_project, _ = create_mock_coro("adapters.repository.TodoRepository.user_in_project")
    mock_user_in_project.return_value = True
    perm_service = DeveloperPermService(fake_repo)
    user_id = 100
    project_id = 200

    result = await perm_service._memberof(user_id=user_id, project_id=project_id)

    assert result is True
    mock_user_in_project.assert_called_once_with(fake_repo, user_id=user_id, project_id=project_id)


@pytest.mark.asyncio
async def test_memberof_returns_false_when_user_not_in_project(fake_repo, create_mock_coro):
    mock_user_in_project, _ = create_mock_coro("adapters.repository.TodoRepository.user_in_project")
    mock_user_in_project.return_value = False
    perm_service = DeveloperPermService(fake_repo)
    user_id = 100
    project_id = 200

    result = await perm_service._memberof(user_id=user_id, project_id=project_id)

    assert result is False
    mock_user_in_project.assert_called_once_with(fake_repo, user_id=user_id, project_id=project_id)


@pytest.mark.asyncio
async def test_owns_returns_true(fake_repo, create_mock_coro):
    mock_get_project_by_id, _ = create_mock_coro("adapters.repository.TodoRepository.get_project_by_id")
    mock_get_project_by_id.return_value = schemas.ProjectInDb(owner=100, title="test project", id=1, created_at=datetime.now())
    perm_service = DeveloperPermService(fake_repo)
    user_id = 100
    project_id = 200

    result = await perm_service._owns(user_id=user_id, project_id=project_id)

    assert result is True
    mock_get_project_by_id.assert_called_once_with(fake_repo, project_id)


@pytest.mark.asyncio
async def test_owns_returns_true(fake_repo, create_mock_coro):
    mock_get_project_by_id, _ = create_mock_coro("adapters.repository.TodoRepository.get_project_by_id")
    mock_get_project_by_id.return_value = schemas.ProjectInDb(owner=100, title="test project", id=1, created_at=datetime.now())
    perm_service = DeveloperPermService(fake_repo)
    user_id = 100
    project_id = 200

    result = await perm_service._owns(user_id=user_id, project_id=project_id)

    assert result is True
    mock_get_project_by_id.assert_called_once_with(fake_repo, project_id)


@pytest.mark.asyncio
async def test_owns_returns_false(fake_repo, create_mock_coro):
    mock_get_project_by_id, _ = create_mock_coro("adapters.repository.TodoRepository.get_project_by_id")
    mock_get_project_by_id.return_value = schemas.ProjectInDb(owner=101, title="test project", id=1, created_at=datetime.now())
    perm_service = DeveloperPermService(fake_repo)
    user_id = 100
    project_id = 200

    result = await perm_service._owns(user_id=user_id, project_id=project_id)

    assert result is False
    mock_get_project_by_id.assert_called_once_with(fake_repo, project_id)
