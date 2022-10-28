from jwt_utils import JWTUtils

from passlib.context import CryptContext

import schemas
from core import config
from services import exceptions as exc
from services.base import BaseService
from models import User


settings = config.get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_utils = JWTUtils(secret=settings.SECRET_KEY)


def hash(pwd: str) -> str:
    return pwd_context.hash(pwd)


def verify_hash(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class UserService(BaseService):
    async def _authenticate(self, username: str, password: str) -> schemas.UserInDb:
        user = await self.repo.get_by_username(username)
        if not user:
            raise exc.NotFound("user does not exist.")
        if not verify_hash(password, user.password):
            raise exc.LoginError("invalid username or password.")
        return user

    def _create_access_token(self, user: schemas.User) -> str:
        to_encode = {
            "sub": user.username, 
            "uid": user.id,
            "role": user.role
        }
        return jwt_utils.create_token(to_encode)

    async def login(self, username: str, password: str) -> schemas.Token:
        return schemas.Token(
            access_token=self._create_access_token(
                await self._authenticate(username, password)),
            token_type="Bearer")

    async def create_user(self, user: schemas.UserCreate) -> schemas.User:
        if await self.repo.get_by_username(user.username):
            raise exc.UniqueViolationError("username is taken.")

        db_user = User(
            username=user.username,
            password=hash(user.password),
            role=user.role.value)
        return await self.repo.create(db_user)

