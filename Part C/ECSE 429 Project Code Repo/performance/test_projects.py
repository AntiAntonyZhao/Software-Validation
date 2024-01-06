from tests.projects.test_projects import *

from . import ITERATION_NUM
import random

def test_add_projects(client):
    for _ in range(1, ITERATION_NUM + 1):
        project_create_json["title"] = f"Post new title 1 + {random.randint(0, 1000)}"
        curl("POST", PROJECTS, "json", "json", json=project_create_json)


def test_update_projects(client):
    for index in range(1, ITERATION_NUM + 1):
        curl(
            "PUT", PROJECTS + f"/{index}", "json", "json", json.dumps({"title": f"Post new title 1 + {random.randint(0, 1000)}"})
        )


def test_delete_projects(client):
    for index in range(1, ITERATION_NUM + 1):
        curl("DELETE", PROJECTS + f"/{index}")
