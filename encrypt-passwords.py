from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from starlette import status


class AuthHandler:
    def __init__(self) -> None:
        self.security = HTTPBearer()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret: str = "05d429c843a04ae63b4521916a3ea9a99eeaabcf6a47d75161663f58cf042805f8490a9445ce894eaa6bda11046e718986fd4dcc0c829b616e14d2cf9a556654b1c179e721ce7cf2ceb44900c41ed680fb70da8f7b9dcdd72db4fa9a863335f96b4079e882a87dae0183aff20081227f46c816fe8daff315369337a5c331dcad2a1be65f1cc2b81cadc8f459f4f147dd12e4471f194154119ab86a22e44e6ed60906ba827fde716ca9771d048753fe43bb5a7a22f92284e65e6e6faaafbce31fc47fc625ac34e777ec5164b2f31e7e0faead9a7933bd0b616d974c060766864ebc688923f001c2296d45170ae3aff30945f2d524d820436ca81ee17494eb031d"

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password, scheme="bcrypt")

    def encode_token(self, user_id: int, user_email: str) -> str:
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


def format_sql_query(hashed_passwords: list[str]) -> str:
    return f"""
    INSERT INTO users (id, email, password, is_verified, balance, name, created_at) VALUES
  (gen_random_uuid(), 'user1@example.com', '{hashed_passwords[0]}', false, 1000, 'User One', NOW()),
  (gen_random_uuid(), 'user2@example.com', '{hashed_passwords[1]}', false, 1000, 'User Two', NOW()),
  (gen_random_uuid(), 'user3@example.com', '{hashed_passwords[2]}', false, 1000, 'User Three', NOW()),
  (gen_random_uuid(), 'user4@example.com', '{hashed_passwords[3]}', false, 1000, 'User Four', NOW()),
  (gen_random_uuid(), 'user5@example.com', '{hashed_passwords[4]}', false, 1000, 'User Five', NOW()),
  (gen_random_uuid(), 'user6@example.com', '{hashed_passwords[5]}', false, 1000, 'User Six', NOW()),
  (gen_random_uuid(), 'user7@example.com', '{hashed_passwords[6]}', false, 1000, 'User Seven', NOW()),
  (gen_random_uuid(), 'user8@example.com', '{hashed_passwords[7]}', false, 1000, 'User Eight', NOW()),
  (gen_random_uuid(), 'user9@example.com', '{hashed_passwords[8]}', false, 1000, 'User Nine', NOW()),
  (gen_random_uuid(), 'user10@example.com','{hashed_passwords[9]}', false, 1000, 'User Ten', NOW());
"""


print(
    format_sql_query(
        [
            AuthHandler().get_password_hash(pswd)
            for pswd in [
                "password1",
                "password2",
                "password3",
                "password4",
                "password5",
                "password6",
                "password7",
                "password8",
                "password9",
                "password10",
            ]
        ]
    )
)
