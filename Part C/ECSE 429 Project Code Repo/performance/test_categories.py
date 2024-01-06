import random
from tests.categories.test_categories import *

from . import ITERATION_NUM


def test_add_categories(client):
    for _ in range(1, ITERATION_NUM + 1):
        categories_post_data["title"] = f"Post new title 1 + {random.randint(0, ITERATION_NUM)}"
        categories_post_data["description"] = f"Post new description 1 + {random.randint(0, ITERATION_NUM)}"
        curl(
            "POST", CATEGORIES, "json", "json", json.dumps(categories_post_data)
        )


def test_update_categories(client):
    for index in range(1, ITERATION_NUM + 1):
        curl(
            "PUT", CATEGORIES + f"/{index}", "json", "json", json.dumps({"title": f"Post new title 1 + {random.randint(0, ITERATION_NUM)}"})
        )


def test_delete_categories(client):
    for index in range(1, ITERATION_NUM + 1):
        curl("DELETE", CATEGORIES + f"/{index}")
