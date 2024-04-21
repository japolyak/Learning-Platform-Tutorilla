import requests
from bot.config import api_link
from typing import Literal
from bot.api.api_models import Role


class SubjectClient:
    __link = f"{api_link}/subjects"

    @classmethod
    def get_users_subjects(cls, user_id: int, role: Literal[Role.Student, Role.Tutor], is_available: bool):
        url = f"{cls.__link}/users/{user_id}/available/{is_available}/?role={role}"
        r = requests.get(url)

        return r
