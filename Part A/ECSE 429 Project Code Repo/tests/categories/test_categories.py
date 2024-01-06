import json

from ..config import CATEGORIES
from ..utils import curl, sort_json
from .category_test_data import *

cate = "categories"

# /categories ---3
def test_get_categories(client):
    code, content = curl("GET", CATEGORIES, "", "json")
    assert code == 200 and sort_json(content) == sort_json(categories_get_response)


def test_head_categories(client):
    code, content = curl("HEAD", CATEGORIES, "", "")
    assert code == 200


def test_post_categories(client):
    code, content = curl(
        "POST", CATEGORIES, "json", "json", json.dumps(categories_post_data)
    )
    code2, content2 = curl("GET", CATEGORIES, "", "json")
    assert code == 201 and len(content2[cate]) == 3


# /categories/:id ---9
def test_get_categories_id1(client):
    code, content = curl("GET", CATEGORIES + "/1", "", "json")
    assert code == 200 and sort_json(content) == sort_json(categories_get_response1)


def test_get_categories_id6(client):
    code, content = curl("GET", CATEGORIES + "/6", "", "")
    assert code == 404


def test_head_categories_id(client):
    code, content = curl("HEAD", CATEGORIES + "/1", "", "")
    assert code == 200


def test_post_categories_id1(client):
    code, content = curl(
        "POST", CATEGORIES + "/1", "json", "json", json.dumps(categories_post_data)
    )
    code2, content2 = curl("GET", CATEGORIES, "", "json")
    assert code == 200 and len(content2[cate]) == 2


def test_post_categories_id6(client):
    code, content = curl(
        "POST", CATEGORIES + "/6", "json", "json", json.dumps(categories_post_data)
    )
    code2, content2 = curl("GET", CATEGORIES, "", "json")
    assert code == 404 and len(content2[cate]) == 2


def test_put_categories_id1(client):
    code, content = curl(
        "PUT", CATEGORIES + "/1", "json", "json", json.dumps(categories_post_data)
    )
    code2, content2 = curl("GET", CATEGORIES, "", "json")
    assert code == 200 and len(content2[cate]) == 2


def test_put_categories_id6(client):
    code, content = curl(
        "PUT", CATEGORIES + "/6", "json", "json", json.dumps(categories_post_data)
    )
    code2, content2 = curl("GET", CATEGORIES, "", "json")
    assert code == 404 and len(content2[cate]) == 2


def test_delete_categories_id2(client):
    code, content = curl("DELETE", CATEGORIES + "/2", "", "")
    code2, content2 = curl("GET", CATEGORIES, "", "json")
    assert code == 200 and len(content2[cate]) == 1


def test_delete_categories_id10(client):
    code, content = curl("DELETE", CATEGORIES + "/10", "", "")
    code2, content2 = curl("GET", CATEGORIES, "", "json")
    assert code == 404 and len(content2[cate]) == 2


# /categories/:id/todos ---7
def test_get_categories_id1_todos(client):
    code, content = curl("GET", CATEGORIES + "/1" + "/todos", "", "json")
    assert code == 200 and len(content["todos"]) == 0


def test_get_categories_id6_todos(client):
    code, content = curl("GET", CATEGORIES + "/6" + "/todos", "", "json")
    assert code == 404


def test_head_categories_id1_todos(client):
    code, content = curl("GET", CATEGORIES + "/1" + "/todos", "", "json")
    assert code == 200


def test_post_categories_id1_todos(client):
    code0, content0 = curl("GET", CATEGORIES + "/1" + "/todos", "", "json")
    code, content = curl(
        "POST",
        CATEGORIES + "/1" + "/todos",
        "json",
        "json",
        json.dumps(categories_todos_post_data),
    )
    code1, content1 = curl("GET", CATEGORIES + "/1" + "/todos", "", "json")
    assert code == 201 and len(content1["todos"]) == len(content0["todos"]) + 1


def test_post_categories_id6_todos(client):
    code, content = curl(
        "POST",
        CATEGORIES + "/6" + "/todos",
        "json",
        "json",
        json.dumps(categories_todos_post_data),
    )
    assert code == 404


def test_delete_categories_id1_todos_id3(client):
    code0, content0 = curl(
        "POST",
        CATEGORIES + "/1" + "/todos",
        "json",
        "json",
        json.dumps(categories_todos_post_data),
    )
    code, content = curl("DELETE", CATEGORIES + "/1/todos/3", "", "")
    code2, content2 = curl("GET", CATEGORIES + "/1" + "/todos", "", "json")
    assert code == 200 and len(content2["todos"]) == 0


def test_delete_categories_id6_todos_id3(client):
    code0, content0 = curl(
        "POST",
        CATEGORIES + "/6" + "/todos",
        "json",
        "json",
        json.dumps(categories_todos_post_data),
    )
    code, content = curl("DELETE", CATEGORIES + "/6/todos/3", "", "")
    assert code0 == 404 and code == 404


# /categories/:id/projects ---7
def test_get_categories_id1_projects(client):
    code, content = curl("GET", CATEGORIES + "/1" + "/projects", "", "json")
    assert code == 200 and len(content["projects"]) == 0


def test_get_categories_id6_projects(client):
    code, content = curl("GET", CATEGORIES + "/6" + "/projects", "", "json")
    assert code == 404


def test_head_categories_id1_projects(client):
    code, content = curl("GET", CATEGORIES + "/1" + "/projects", "", "json")
    assert code == 200


def test_post_categories_id1_projects(client):
    code0, content0 = curl("GET", CATEGORIES + "/1/projects", "", "json")
    code, content = curl(
        "POST",
        CATEGORIES + "/1/projects",
        "json",
        "json",
        json.dumps(categories_projects_post_data),
    )
    code1, content1 = curl("GET", CATEGORIES + "/1" + "/projects", "", "json")
    assert code == 201 and len(content1["projects"]) == len(content0["projects"]) + 1


def test_post_categories_id6_projects(client):
    code, content = curl(
        "POST",
        CATEGORIES + "/6/projects",
        "json",
        "json",
        json.dumps(categories_todos_post_data),
    )
    assert code == 404


def test_delete_categories_id1_projects_id3(client):
    code0, content0 = curl(
        "POST",
        CATEGORIES + "/1" + "/projects",
        "json",
        "json",
        json.dumps(categories_projects_post_data),
    )
    code, content = curl("DELETE", CATEGORIES + "/1/projects/2", "", "")
    code2, content2 = curl("GET", CATEGORIES + "/1/projects", "", "json")
    assert code == 200 and len(content2["projects"]) == 0


def test_delete_categories_id6_projects_id3(client):
    code0, content0 = curl(
        "POST",
        CATEGORIES + "/6" + "/projects",
        "json",
        "json",
        json.dumps(categories_todos_post_data),
    )
    code, content = curl("DELETE", CATEGORIES + "/6/projects/3", "", "")
    assert code == 404 and code0 == 404


# uncocumented tests ---6


def test_put_categories(client):
    code, content = curl(
        "PUT", CATEGORIES, "json", "json", json.dumps(categories_post_data)
    )
    assert code == 405


def test_put_categories_id1_todos(client):
    code, content = curl(
        "PUT",
        CATEGORIES + "/1/todos",
        "json",
        "json",
        json.dumps(categories_todos_post_data),
    )
    assert code == 405


def test_put_categories_id1_projects(client):
    code, content = curl(
        "PUT",
        CATEGORIES + "/1/projects",
        "json",
        "json",
        json.dumps(categories_todos_post_data),
    )
    assert code == 405


def test_delete_categories(client):
    code, content = curl("DELETE", CATEGORIES, "", "")
    code2, content2 = curl("GET", CATEGORIES, "", "json")
    assert code == 405 and len(content2[cate]) == 2


def test_delete_categories_id1_todos(client):
    code0, content0 = curl(
        "POST",
        CATEGORIES + "/1" + "/todos",
        "json",
        "json",
        json.dumps(categories_todos_post_data),
    )
    code, content = curl("DELETE", CATEGORIES + "/1/todos", "", "")
    code2, content2 = curl("GET", CATEGORIES + "/1" + "/todos", "", "json")
    assert code == 405 and len(content2["todos"]) == 1


def test_delete_categories_id1_projects(client):
    code0, content0 = curl(
        "POST",
        CATEGORIES + "/1/projects",
        "json",
        "json",
        json.dumps(categories_projects_post_data),
    )
    code, content = curl("DELETE", CATEGORIES + "/1/todos", "", "")
    code2, content2 = curl("GET", CATEGORIES + "/1" + "/projects", "", "json")
    assert code == 405 and len(content2["projects"]) == 1
