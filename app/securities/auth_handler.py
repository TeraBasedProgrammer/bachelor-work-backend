from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from starlette import status

from app.config.settings.base import settings


class AuthHandler:
    def __init__(self) -> None:
        self.security = HTTPBearer()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret: str = settings.JWT_SECRET

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password, scheme="bcrypt")

    def encode_token(self, user_id: str, user_email: str) -> str:
        # Initialize user_crud object to get user id once and put it in jwt payload

        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=30),
            "iat": datetime.now(timezone.utc),
            "sub": user_email,
            "id": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token: str) -> Optional[Dict[str, bool]]:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return {"email": payload["sub"], "id": payload["id"], "auth0": False}
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, detail="Signature has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def get_auth_handler() -> AuthHandler:
    return AuthHandler()


auth_handler: AuthHandler = get_auth_handler()
