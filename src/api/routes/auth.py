from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import schemas
from services import exceptions as exc
from api.deps.service import get_service
from adapters.repository import UserRepository
from services.users import UserService


router = APIRouter(tags=["auth"])

@router.post("/users")
async def signup(
    user: schemas.UserCreate,
    user_svc: UserService = Depends(get_service(repo_type=UserRepository, service_type=UserService))
) -> schemas.User:
        try:
            return await user_svc.create_user(user)
        except exc.UniqueViolationError as e:
            raise HTTPException(status_code=400, detail=str(e))


@router.post("/token", response_model=schemas.Token)
async def login(
    user_svc: UserService = Depends(get_service(repo_type=UserRepository, service_type=UserService)),
    form_data: OAuth2PasswordRequestForm=Depends()
) -> schemas.Token:
    try:
        return await user_svc.login(
            form_data.username, form_data.password)
    except exc.NotFound as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"})
    except exc.LoginError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"})
