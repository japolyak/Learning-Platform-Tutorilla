import requests
from ..config import api_link
import logging


class SessionApi:
    base_url = 'session/'

    @staticmethod
    def get_session(tg_id: int) -> dict:
        url = f"{api_link}{SessionApi.base_url}{tg_id}/"

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()
            return data
        except requests.RequestException as e:
            logging.error(e)
            return {}
