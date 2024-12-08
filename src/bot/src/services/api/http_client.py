from requests import Response, Session
from requests.cookies import RequestsCookieJar
from typing import Optional, Union, Generic, Type, Any, Tuple
from telebot.types import Message, CallbackQuery

from src.common.models import T, ErrorDto, TokenDto
from src.common.config import api_link
from src.common.telegram_init_data import TelegramInitData
from src.common.storage import Storage


class ApiResponse(Generic[T]):
    def __init__(self, data: Optional[T] = None, error: Optional[ErrorDto] = None):
        self.__success = data is not None
        self.data = data
        self.error = error

    def is_successful(self) -> bool:
        return self.__success


class HTTPClient:
    __base_url = api_link
    access_token: Optional[str] = None

    def __init__(self, url: str):
        self.module_url = f"{self.__base_url}/{url}/"
        self.session = Session()

    def check_session(self, **kwargs):
        if kwargs["tg_data"] is None:
            raise Exception('No TG data was passed')

        tg_data: Optional[Union[Message, CallbackQuery]] = kwargs["tg_data"]

        access_token = Storage().get_access_token(tg_data.from_user.id)

        if access_token is None:
            session_key = Storage().get_session_key(tg_data.from_user.id)

            if session_key is None:
                init_data = TelegramInitData().create_str_init_data(tg_data, {"from_bot": True})

                access_token, session_key = self.__authenticate(init_data)
            else:
                access_token, session_key = self.__refresh_access_token(session_key)
                Storage().delete_old_session(tg_data.from_user.id, session_key)

            if session_key:
                Storage().set_user_session(tg_data.from_user.id, access_token, session_key)
                self.session.cookies.set("sessionKey", session_key)

        self.access_token = access_token

        return self

    def __authenticate(self, init_data: str) -> Tuple[str, Optional[str]]:
        headers = {
            "Init-Data": init_data,
        }

        response = self.session.request(
            method="GET",
            url=self.__base_url + "/auth/me/",
            headers=headers
        )

        result, cookies = self.__response(response, TokenDto)

        if not result.is_successful() or result.data is None:
            raise Exception('No tokens:(')

        return result.data.access_token, cookies.get("sessionKey")

    def __refresh_access_token(self, session_key: str) -> Tuple[str, str]:
        headers = {
            "SessionKey": session_key
        }

        response = self.session.request(
            method="GET",
            url=self.__base_url + "/auth/refresh/",
            headers=headers
        )

        result, cookies = self.__response(response, TokenDto)

        if not result.is_successful() or result.data is None:
            raise Exception('No tokens:(')

        return result.data.access_token, cookies.get("sessionKey")

    def request(self, method, url, model_class: Type[T], **kwargs):
        data = kwargs.get("data")
        passed_headers: Optional[dict] = kwargs.get("headers")

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        if passed_headers is not None:
            headers.update(**passed_headers)

        response = self.session.request(
            method=method,
            url=self.module_url + url,
            data=data,
            headers=headers
        )

        return self.__response(response, model_class)[0]

    @classmethod
    def __response(cls, response: Response, model_class: Type[T]) ->Tuple[ApiResponse[T], Optional[RequestsCookieJar]]:
        if not response.ok:
            error = ErrorDto(**response.json())
            return ApiResponse[T](error=error), None

        # TODO - rethink implementation
        if model_class is None and response.ok:
            return ApiResponse[T](data=Any), response.cookies

        json_data = response.json()
        data = model_class(**json_data)

        return ApiResponse[T](data=data), response.cookies

    def get(self, url, model_class: Type[T], **kwargs):
        return self.request("GET", url, model_class, **kwargs)

    def post(self, url, model_class: Type[T], **kwargs):
        return self.request("POST", url, model_class, **kwargs)

    def put(self, url, model_class: Type[T], **kwargs):
        return self.request("PUT", url, model_class, **kwargs)

    def delete(self, model_class: Type[T], url, **kwargs):
        return self.request("DELETE", url, model_class, **kwargs)
