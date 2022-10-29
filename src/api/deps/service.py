from typing import Callable, Type

from fastapi import Depends

import schemas
from services.base import BaseService
from services.permissions import PermService, DeveloperPermService, ManagerPermService
from adapters.repository import BaseRepository
from api.deps.db import get_repository
from api.deps.auth import current_user


def get_service(*,
    repo_type: Type[BaseRepository],
    service_type: Type[BaseService],
) -> Callable:
    def _get_service(
        repo: BaseRepository = Depends(get_repository(repo_type)),
    ) -> Type[BaseService]:
        return service_type(repo)

    def _get_permissions_service(
        repo: BaseRepository = Depends(get_repository(repo_type)),
        user: schemas.User = Depends(current_user)
    ) -> Type[BaseService]:
        return DeveloperPermService(repo) \
                if user.role == schemas.Role.DEV \
                else ManagerPermService(repo)
    
    return _get_permissions_service \
        if issubclass(service_type, PermService) \
        else _get_service
