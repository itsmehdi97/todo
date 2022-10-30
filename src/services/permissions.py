import abc

import schemas
from services.base import BaseService
from services import exceptions as exc


class PermService(BaseService):
    async def _memberof(self, *, user_id: int, project_id: int) -> bool:
        return await self.repo.user_in_project(
            user_id=user_id, project_id=project_id)

    async def _owns(self, *, user_id: int, project_id: int) -> bool:
        project = await self.repo.get_project_by_id(project_id)
        return project.owner == user_id

    @abc.abstractmethod
    async def can_view_project_tasks(self, *, project_id: int, request_user: schemas.User) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def can_create_project(self, *, request_user: schemas.User) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def can_create_task(self, *, project_id: int, request_user: schemas.User) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def can_assign_task(self, *, task_id: int, request_user: schemas.User) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    async def can_assign_project(self, *, request_user: schemas.User) -> bool:
        raise NotImplementedError()


class ManagerPermService(PermService):
    async def can_view_project_tasks(self, *, project_id: int, request_user: schemas.User) -> bool:
        return await self._owns(user_id=request_user.id, project_id=project_id)

    async def can_create_project(self, *, request_user: schemas.User) -> bool:
        return True

    async def can_create_task(self, *, project_id: int, request_user: schemas.User) -> bool:
        return await self._owns(user_id=request_user.id, project_id=project_id)

    async def can_assign_task(self, *, task_id: int, request_user: schemas.User) -> bool:
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise exc.NotFound("task not found")
        return await self._owns(user_id=request_user.id, project_id=task.project_id)

    async def can_assign_project(self, *, project_id: int, request_user: schemas.User) -> bool:
        return await self._owns(user_id=request_user.id, project_id=project_id)


class DeveloperPermService(PermService):
    async def can_view_project_tasks(self, *, project_id: int, request_user: schemas.User) -> bool:
        return await self._memberof(user_id=request_user.id, project_id=project_id)

    async def can_create_project(self, *, request_user: schemas.User) -> bool:
        return False

    async def can_create_task(self, *, project_id: int, request_user: schemas.User) -> bool:
        return await self._memberof(user_id=request_user.id, project_id=project_id)

    async def can_assign_task(self, *, task_id: int, request_user: schemas.User) -> bool:
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise exc.NotFound("task not found")
        return await self._memberof(user_id=request_user.id, project_id=task.project_id)

    async def can_assign_project(self, *, project_id: int, request_user: schemas.User) -> bool:
        return False
