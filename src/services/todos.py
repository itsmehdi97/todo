import abc
from typing import List, Optional

import schemas
from services import exceptions as exc
from services.base import BaseService
import models


class TodoService(BaseService):
    @abc.abstractmethod
    async def create_task(
        self, task: schemas.TaskCreate, *, request_user: schemas.User
    ) -> models.Task:
        raise NotImplementedError()

    @abc.abstractmethod
    async def assign_task(
        self, *, task_id: int, user_id: int, request_user=schemas.User
    ) -> None:
        raise NotImplementedError()
    
    @abc.abstractmethod
    async def assign_project(
        self, *, project_id: int, user_id: int, request_user=schemas.User
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def create_project(
        self, project: schemas.ProjectCreate, *, request_user: schemas.User
    ) -> models.Project:
        raise NotImplementedError()

    async def project_tasks(
        self,
        *,
        project_id: int,
        request_user: schemas.User,
        user_id: Optional[int] = None
    ) -> List[models.Task]:
        raise NotImplementedError()

    async def user_memberof_project(self, *, user_id: int, project_id: int) -> bool:
        return await self.repo.user_in_project(
            user_id=user_id, project_id=project_id)
    
    async def user_owns_project(self, project_id: int, user_id: int) -> bool:
        project = await self.repo.get_project_by_id(project_id)
        return project.owner == user_id


class DeveloperTodoService(TodoService):
    async def create_project(
        self, project: schemas.ProjectCreate, *, request_user: schemas.User
    ) -> models.Project:
        raise exc.OperationNotPermitted("developers can't create projects.")
    
    async def assign_project(
        self, *, project_id: int, user_id: int, request_user=schemas.User
    ) -> None:
        raise exc.OperationNotPermitted("developers can't assign projects.")

    async def create_task(
        self, task: schemas.TaskCreate, *, request_user: schemas.User
    ) -> models.Task:
        if not await self.user_memberof_project(user_id=request_user.id, project_id=task.project_id):
            raise exc.OperationNotPermitted(
                "developers can create tasks only for their projects.")

        return await self.repo.create_task(task)

    async def get_project_tasks(
        self,
        *,
        project_id: int,
        request_user: schemas.User,
        user_id: Optional[int] = None
    ) -> List[models.Task]:
        project = await self.repo.get_project_by_id(project_id)
        if not project:
            raise exc.NotFound("project not found.")

        if not await self.user_memberof_project(user_id=request_user.id, project_id=project_id):
            raise exc.OperationNotPermitted(
                "only project's members or owners can access its tasks.")
        
        return await self.repo.get_project_tasks(project_id, user_id=user_id)

    async def assign_task(
        self, *, task_id: int, user_id: int, request_user=schemas.User
    ) -> None:
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise exc.NotFound("task not found.")
        if not user_id == request_user.id:
            raise exc.OperationNotPermitted(
                "developers can only assign tasks to themselves.")
        if not await self.user_memberof_project(user_id=request_user.id, project_id=task.project_id):
            raise exc.OperationNotPermitted(
                "developers can only take tasks from their projects.")
        
        await self.repo.asign_task(task_id=task_id, user_id=user_id)


class ManagerTodoService(TodoService):
    async def create_task(
        self, task: schemas.TaskCreate, *, request_user: schemas.User
    ) -> models.Task:
        if not await self.user_owns_project(project_id=task.project_id, user_id=request_user.id):
            raise exc.OperationNotPermitted(
                "managers can only create tasks in their own projects.")

        return await self.repo.create_task(task)

    async def assign_task(
        self, *, task_id: int, user_id: int, request_user=schemas.User
    ) -> None:
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise exc.NotFound("task not found.")
        if not await self.user_memberof_project(user_id=user_id, project_id=task.project_id):
            raise exc.OperationNotPermitted(
                "developer is not member of this project.")
        if not await self.user_owns_project(user_id=request_user.id, project_id=task.project_id):
            raise exc.OperationNotPermitted(
                "managers can only assign tasks from their own projects.")
        
        await self.repo.asign_task(task_id=task_id, user_id=user_id)

    async def assign_project(
        self, *, project_id: int, user_id: int, request_user=schemas.User
    ) -> None:
        if not await self.user_owns_project(user_id=request_user.id, project_id=project_id):
            raise exc.OperationNotPermitted(
                "managers can only assign to their own projects.")
        
        await self.repo.assign_project(project_id=project_id, user_id=user_id)
        
    
    async def create_project(
        self, project: schemas.ProjectCreate, *, request_user: schemas.User
    ) -> models.Project:
        project.owner = request_user.id
        return await self.repo.create_project(project)

    async def get_project_tasks(
        self,
        *,
        project_id: int,
        request_user: schemas.User,
        user_id: Optional[int] = None
    ) -> List[models.Task]:
        project = await self.repo.get_project_by_id(project_id)
        if not project:
            raise exc.NotFound("project not found.")

        if not await self.user_owns_project(project_id=project.id, user_id=request_user.id):
            raise exc.OperationNotPermitted(
                "only project's members or owners can access its tasks.")
        
        return await self.repo.get_project_tasks(project_id, user_id=user_id)
