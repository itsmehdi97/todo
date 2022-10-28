from typing import List, Optional
from urllib import request

from fastapi import APIRouter, Depends, HTTPException

import schemas
from services import exceptions as exc
from api.deps.service import get_service
from api.deps.auth import current_user
from adapters.repository import TodoRepository

from services.todos import TodoService


router = APIRouter(tags=["tasks"])


@router.get("/projects/{project_id}/tasks")
async def project_tasks(
    project_id: int,
    user_id: Optional[int] = None,
    task_svc: TodoService = Depends(get_service(repo_type=TodoRepository, service_type=TodoService)),
    user: schemas.User = Depends(current_user)
) -> List[schemas.TaskInDb]:
    try:
        return await task_svc.get_project_tasks(
            project_id=project_id, request_user=user, user_id=user_id)
    except exc.NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exc.OperationNotPermitted as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/tasks/assign")
async def assign_task(
    assignment: schemas.TaskAssignment,
    todo_svc: TodoService = Depends(get_service(repo_type=TodoRepository, service_type=TodoService)),
    user: schemas.User = Depends(current_user)
) -> None:

    await todo_svc.assign_task(
        task_id=assignment.task_id, user_id=assignment.user_id, request_user=user)
