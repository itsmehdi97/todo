import abc
from typing import List, Type, Generic, TypeVar, Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy import func

from db import Session
import models
import schemas



class BaseRepository(abc.ABC):
    def __init__(self, db: Session):
        self.db = db


class UserRepository(BaseRepository):
    model = models.User

    async def create(self, user: models.User) -> models.User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_username(self, username: str) -> models.User:
        result = await self.db.execute(select(models.User) \
            .where(models.User.username == username))
        return result.scalar()

class TodoRepository(BaseRepository):
    async def get_project_tasks(self, project_id: int, user_id: Optional[int] = None) -> List[models.Task]:
        q = select(models.Task) \
            .where(models.Task.project_id == project_id)
        if user_id:
            q = q.join(models.UsersTasks, onclause=models.UsersTasks.task_id==models.Task.id) \
                .where(models.UsersTasks.user_id == user_id)

        result = await self.db.execute(q)
        return result.scalars().all()

    async def get_project_by_id(self, id: int) -> models.Project:
        result = await self.db.execute(select(models.Project).where(models.Project.id == id))
        return result.scalar()
    
    async def get_task_by_id(self, id: int) -> models.Task:
        result = await self.db.execute(select(models.Task).where(models.Task.id == id))
        return result.scalar()

    async def create_task(self, task: schemas.TaskCreate) -> models.Task:
        db_task = models.Task(**task.dict())
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh()
        return db_task
    
    async def asign_task(self, *, task_id: int, user_id: int) -> None:
        assignment = models.UsersTasks(user_id=user_id, task_id=task_id)
        self.db.add(assignment)
        await self.db.commit()
    
    async def assign_project(self, project_id: int, user_id: int) -> None:
        membership = models.UsersProjects(user_id=user_id, project_id=project_id)
        self.db.add(membership)
        await self.db.commit()
    
    async def create_project(self, project: schemas.ProjectCreate) -> models.Project:
        db_project = models.Project(**project.dict())
        self.db.add(db_project)
        await self.db.commit()
        await self.db.refresh(db_project)
        return db_project

    async def user_in_project(self, *, user_id: int, project_id: int) -> bool:
        q = select(models.UsersProjects.user_id).where(
                models.UsersProjects.user_id==user_id,
                models.UsersProjects.project_id==project_id)
        result = await self.db.execute(q)
        return bool(len(result.all()))
