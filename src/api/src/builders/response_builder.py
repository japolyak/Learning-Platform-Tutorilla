from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Any, Optional

from src.core.config import refresh_token_ttl_in_days
from src.core.logger import log


class ResponseBuilder:
    @classmethod
    def error_response(cls, status_code: int = status.HTTP_400_BAD_REQUEST, message: str = 'Bad request'):
        log.error(msg=message)
        return JSONResponse(status_code=status_code, content=jsonable_encoder({"detail": message}))

    @classmethod
    def success_response(cls, status_code: int = status.HTTP_200_OK, content: Any = None, cookies: Optional[dict] = None):
        if not content:
            response = Response(status_code=status_code)
        else:
            response = JSONResponse(status_code=status_code, content=jsonable_encoder(content))

        if cookies:
            for key, value in cookies.items():
                response.set_cookie(
                    key=key,
                    value=value,
                    httponly=True,
                    secure=True,
                    samesite="none",
                    max_age=86400 * refresh_token_ttl_in_days
                )

        return response
