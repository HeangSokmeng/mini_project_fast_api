# app/helpers/response_helper.py
from typing import Any, Optional

from fastapi import status
from fastapi.responses import JSONResponse


class ResponseHelper:
    @staticmethod
    def success_response(
        data: Any = None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data,
                "error": None
            }
        )

    @staticmethod
    def error_response(
        message: str = "Error occurred",
        error: Optional[str] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Any = None
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "data": data,
                "error": error
            }
        )

    @staticmethod
    def unauthorized_response(message: str = "Unauthorized") -> JSONResponse:
        return ResponseHelper.error_response(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def forbidden_response(message: str = "Insufficient permissions") -> JSONResponse:
        return ResponseHelper.error_response(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )
