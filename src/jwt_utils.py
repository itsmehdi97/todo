import json
from typing import Optional
from datetime import datetime, timezone, timedelta

from core.config import Settings, get_settings

from jose import jws, jwt
from jose.utils import base64url_decode


settings = get_settings()


class JWTUtils:
    def __init__(self, secret: str):
        self.secret = secret

    def verify(self, token: str) -> Optional[dict]:
        encoded_header, _, _ = token.split(".")
        header = json.loads(base64url_decode(encoded_header).decode())
        bytes_payload = jws.verify(token, self.secret, algorithms=[header["alg"]])
        payload = json.loads(bytes_payload.decode())
        if self._is_expired(payload.get("exp")):
            return None
        return payload

    def _is_expired(self, ts: float) -> bool:
        return datetime.now(tz=timezone.utc).timestamp() > ts

    def create_token(self, data: dict[str,str]) -> str:
        expire = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        data.update({"exp": datetime.utcnow() + expire})
        return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)