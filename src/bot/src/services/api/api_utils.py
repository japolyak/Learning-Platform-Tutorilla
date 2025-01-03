from requests import Response
from typing import Generic, Type, Optional, Any

from src.core.models import T, ErrorDto


class ApiResponse(Generic[T]):
    def __init__(self, data: Optional[T] = None, error: Optional[ErrorDto] = None):
        self.__success = data is not None
        self.data = data
        self.error = error

    def is_successful(self) -> bool:
        return self.__success


class ApiUtils:
    @staticmethod
    def create_api_response(response: Response, model_class: Type[T]) -> ApiResponse[T]:
        if not response.ok:
            error = ErrorDto(**response.json())
            return ApiResponse[T](error=error)

        # TODO - rethink
        if model_class is None and response.ok:
            return ApiResponse[T](data=Any)

        json_data = response.json()
        data = model_class(**json_data)

        return ApiResponse[T](data=data)
