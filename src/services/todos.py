from typing import List, Optional

import models
import schemas
from services import exceptions as exc
from services.base import BaseService


class TodoService(BaseService):
    async def create_task(self, task: schemas.TaskCreate) -> models.Task:
        return await self.repo.create_task(task)

    async def assign_task(self, *, task_id: int, user_id: int) -> None:
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise exc.NotFound("task not found.")
        await self.repo.asign_task(task_id=task_id, user_id=user_id)

    async def assign_project(self, *, project_id: int, user_id: int) -> None:
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
        user_id: Optional[int] = None
    ) -> List[models.Task]:
        project = await self.repo.get_project_by_id(project_id)
        if not project:
            raise exc.NotFound("project not found.")
        return await self.repo.get_project_tasks(project_id, user_id=user_id)
