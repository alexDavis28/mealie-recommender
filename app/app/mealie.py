import requests
from .exceptions import *


class Mealie:
    def __init__(self, api_key: str, url: str):
        self.api_key = api_key
        # Strip trailing slash
        self.base_url = url[:-1] if url.endswith("/") else url
        self._test_api()

    def _api_get_all_recipes(self) -> dict:
        # TODO deal with pagination instead of just getting all
        path = "/api/recipes?perPage=500"
        response = self._api_get(path)
        return response.json()
    
    def _api_get_recipe_data(self, slug: str) -> dict:
        path = "/api/recipes/" + slug
        response = self._api_get(path)
        return response.json()

    def get_recipe_slug_ingredient_text(self, recipe_data: dict) -> dict:
        # Data in format from ._api_get_all_recipes
        # Map slug to ingredients list
        out = {}
        for recipe in recipe_data["items"]:
            slug = recipe["slug"]
            data = self._api_get_recipe_data(slug)
            out[slug] = " ".join([i["note"] for i in data["recipeIngredient"]])
        return out

    def get_recipe_training_data(self) -> dict:
        json_data = self.get_all_recipes()
        training_data = self.get_recipe_slug_ingredient_text(json_data)
        return training_data

    def _test_api(self) -> None:
        path = "/api/app/about"
        self._api_get(path)

    def _api_get(self, path: str) -> requests.Response:
        url = self.base_url + path
        response = requests.get(url, headers={
            "Authorization": f"Bearer {self.api_key}"})
        if response.status_code != 200:
            raise MealieApiError(
                f"Failed to connect to Mealie with code {response.status_code}\n{response.text}")
        return response
