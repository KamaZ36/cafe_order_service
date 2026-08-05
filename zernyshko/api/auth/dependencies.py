from typing import Annotated

from fastapi import Depends, Request


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


CurrentUserIP = Annotated[str, Depends(get_current_user_ip_address)]
