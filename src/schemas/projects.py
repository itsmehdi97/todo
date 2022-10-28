from datetime import datetime
from typing import Optional

from schemas.base import BaseSchema


class ProjectBase(BaseSchema):
    title: str
    owner: int

class ProjectCreate(ProjectBase):
    desc: Optional[str] = None


class ProjectInDb(ProjectBase):
    id: int
    desc: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None