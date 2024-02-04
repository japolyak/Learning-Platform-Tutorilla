import requests
from bot.config import api_link


class PrivateCoursesClient:
    @staticmethod
    def get_classes(private_course_id: int, role: str):
        url = f"{api_link}/private-courses/{private_course_id}/classes/?role={role}"
        r = requests.get(url)

        return r

    @staticmethod
    def get_private_courses_by_course_name(user_id: int, subject_name: str, role: str):
        url = f"{api_link}/private-courses/users/{user_id}/subjects/{subject_name}/?role={role}"
        r = requests.get(url)

        return r
