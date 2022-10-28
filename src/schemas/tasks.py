from datetime import datetime
from typing import Optional

from schemas.base import BaseSchema


class TaskBase(BaseSchema):
    title: str
    project_id: int


class TaskCreate(TaskBase):
    desc: Optional[str] = None


class TaskInDb(TaskBase):
    id: int
    desc: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class TaskAssignment(BaseSchema):
    task_id: int
    user_id: int
