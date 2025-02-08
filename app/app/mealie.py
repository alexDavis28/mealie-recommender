import requests
from .exceptions import *

class Mealie:
    def __init__(self, api_key: str, url: str):
        self.api_key = api_key
        # Strip trailing slash
        self.base_url = url[:-1] if url.endswith("/") else url
        self._test_api()

    def get_all_recipes(self) -> dict:
        path = "/api/recipes"
        response = self._get(path)
        return response.json()

    def _test_api(self) -> None:
        path =  "/api/app/about"
        self._get(path)

    def _get(self, path: str) -> requests.Response:
        url = self.base_url + path
        response = requests.get(url, headers = {"Authorization": f"Bearer {self.api_key}"})
        if response.status_code != 200:
            raise MealieApiError(f"Failed to connect to Mealie with code {response.status_code}.\n{response.text}")
        return response