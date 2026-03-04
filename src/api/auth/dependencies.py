from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request, HTTPException, status

from infrastructure.repositories.session.base import BaseSessionRepository
from core.dependencies import container


async def get_current_user_ip_address(request: Request) -> str:
    real_ip = request.headers.get("X-Real-IP")
    forwarded = request.headers.get("X-Forwarded-For")

    if real_ip:
        ip = real_ip
    elif forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.client.host if request.client else "0.0.0.0"

    return ip


async def get_current_user_id(request: Request) -> UUID:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async with container() as context:
        auth_session_repository = await context.get(BaseSessionRepository)
        auth_session = await auth_session_repository.get_by_session_id(session_id)

    if not auth_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return auth_session.user_id


CurrentUserID = Annotated[UUID, Depends(get_current_user_id)]
CurrentUserIP = Annotated[str, Depends(get_current_user_ip_address)]
