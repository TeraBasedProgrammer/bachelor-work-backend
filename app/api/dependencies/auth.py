from typing import Any, Optional

from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.securities.auth_handler import auth_handler


async def auth_wrapper(
    auth: Optional[HTTPAuthorizationCredentials] = Security(
        HTTPBearer(auto_error=False)
    ),
) -> Optional[dict[str, Any]]:
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    user_data = auth_handler.decode_token(auth.credentials)
    return user_data
