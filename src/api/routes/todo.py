from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

import schemas
from services import exceptions as exc
from api.deps.service import get_service
from api.deps.auth import current_user
from adapters.repository import TodoRepository

from services.todos import TodoService
from services.permissions import PermService


router = APIRouter(tags=["tasks"])


@router.get("/projects/{project_id}/tasks")
async def project_tasks(
    project_id: int,
    user_id: Optional[int] = None,
    todo_svc: TodoService = Depends(get_service(repo_type=TodoRepository, service_type=TodoService)),
    perms_svc: PermService = Depends(get_service(repo_type=TodoRepository, service_type=PermService)),
    user: schemas.User = Depends(current_user)
) -> List[schemas.TaskInDb]:
    if not await perms_svc.can_view_project_tasks(project_id=project_id, request_user=user):
        raise HTTPException(
            status_code=404,
            detail="Operation not permitted")
    try:
        return await todo_svc.get_project_tasks(
            project_id=project_id, user_id=user_id)
    except exc.NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/tasks/assign")
async def assign_task(
    assignment: schemas.TaskAssignment,
    todo_svc: TodoService = Depends(get_service(repo_type=TodoRepository, service_type=TodoService)),
    perms_svc: PermService = Depends(get_service(repo_type=TodoRepository, service_type=PermService)),
    user: schemas.User = Depends(current_user)
) -> None:
    if not await perms_svc.can_assign_task(task_id=assignment.task_id, request_user=user):
        raise HTTPException(
            status_code=404,
            detail="Operation not permitted")
    try:
        await todo_svc.assign_task(
            task_id=assignment.task_id, user_id=assignment.user_id, request_user=user)
    except exc.NotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
