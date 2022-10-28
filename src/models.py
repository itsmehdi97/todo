from datetime import datetime

from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    DateTime, String, Integer, Boolean, Text,
    ForeignKey
)

import schemas



mapper_registry = registry()
Base = mapper_registry.generate_base()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now())


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=64), nullable=False, unique=True)
    password = Column(String(length=64), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(length=9), nullable=False)

    tasks = relationship("Task", secondary="users_tasks")


class Project(BaseModel):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=128), nullable=True)
    desc = Column(Text(), nullable=True)
    owner = Column(ForeignKey("user.id"), nullable=False)


class Task(BaseModel):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=128), nullable=True)
    desc = Column(Text(), nullable=True)
    project_id = Column(ForeignKey("project.id"), nullable=False)

    project = relationship(Project)


class UsersProjects(BaseModel):
    __tablename__ = "users_projects"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    project_id = Column(ForeignKey("project.id"), primary_key=True)
    

class UsersTasks(BaseModel):
    __tablename__ = "users_tasks"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    task_id = Column(ForeignKey("task.id"), primary_key=True)
