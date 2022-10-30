
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import schemas
from jwt_utils import JWTUtils
from core.config import get_settings


settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

jwt = JWTUtils(settings.SECRET_KEY)


async def current_user(token: str = Depends(oauth2_scheme)) -> schemas.User:
    payload = jwt.verify(token)
    if payload:
        return schemas.User(
            id=payload.get("uid"), username=payload.get("sub"), role=payload.get("role"))
    raise HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
