from tests.todos.test_todos import *
from . import ITERATION_NUM
import random


def test_add_todos(client):
    for _ in range(1, ITERATION_NUM + 1):
        todos_post_data["title"] = f"Post new title 1 + {random.randint(0, 1000)}"
        curl("POST", TODOS, "json", "json", json.dumps(todos_post_data))


def test_update_todos(client):
    for index in range(1, ITERATION_NUM + 1):
        curl(
            "PUT", TODOS + f"/{index}", "json", "json", json.dumps({"title": f"Post new title 1 + {random.randint(0, 1000)}"})
        )


### Delete ###
def test_delete_todos(client):
    for index in range(1, ITERATION_NUM + 1):
        curl("DELETE", TODOS + f"/{index}")
