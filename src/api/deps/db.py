from typing import Callable, Type

from db import Session
from starlette.requests import Request
from fastapi import Depends

from adapters.repository import BaseRepository


def get_session_factory(request: Request):
    return request.app.state._db


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Session = Depends(get_session_factory)) -> Type[BaseRepository]:
        return Repo_type(db)

    return get_repo
