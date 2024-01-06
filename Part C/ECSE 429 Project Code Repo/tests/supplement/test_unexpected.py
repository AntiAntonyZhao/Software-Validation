import json

import xmltodict

from ..categories.category_test_data import *
from ..config import CATEGORIES, PROJECTS, TODOS
from ..projects.project_test_data import *
from ..todos.todos_test_data import *
from ..utils import curl, sort_json

cate = "categories"


################################################################
########################### TODOS ##############################
################################################################


def test_todos_xml_post_xml_json(client):  # BUG: Not support xml
    code, content = curl("POST", TODOS, "xml", "json", todos_post_data_xml)
    assert code == 400
    assert sort_json(todos_post_response) == sort_json(todos_post_response)
    # {"errorMessages":["java.lang.IllegalStateException: Expected BEGIN_OBJECT but was STRING at line 1 column 1 path $"]}


def test_todos_xml_post_xml_xml(client):  # BUG: Not support xml
    code, content = curl("POST", TODOS, "xml", "xml", todos_post_data_xml)
    assert code == 400 and sort_json(
        xmltodict.parse(todos_post_response_xml)
    ) == sort_json(xmltodict.parse(todos_post_response_xml))
    # <errorMessages>
    # 	<errorMessage>java.lang.IllegalStateException: Expected BEGIN_OBJECT but was STRING at line 1 column 1 path $
    # 	</errorMessage>
    # </errorMessages>


def test_todos_id_put_json_json_title_desc_error(client):
    code, content = curl(
        "PUT",
        TODOS + "/1",
        "json",
        "json",
        json.dumps(
            {
                "title": "title3",
                "description": "Trying to create todo3 using POST",
                "doneStatus": "true",
            }
        ),
    )
    assert code == 400


def test_todos_id_put_json_xml(client):  # BUG: Not support xml
    code, content = curl(
        "PUT", TODOS + "/1", "json", "xml", json.dumps(todos_id_put_data)
    )
    assert code == 400


def test_todos_id_post_json_xml(client):
    code, content = curl(
        "post", TODOS + "/1", "json", "xml", json.dumps(todos_id_put_data)
    )
    assert code == 400  # BUG expected 200


def test_todos_id_categories_get_json_edge_case(client):
    # BUG: continue return 200
    for error_id in [-128, -1, 10000]:  # edge case
        code, _ = curl("GET", TODOS + f"/{error_id}/categories", "", "json")
        assert code == 200


def test_todos_id_categories_get_xml_edge_case(client):
    # BUG: continue return 200
    for error_id in [-128, -1, 10000]:
        code, _ = curl("GET", TODOS + f"/{error_id}/categories", "", "xml")
        assert code == 200


def test_todos_id_categories_head_edge_case(client):
    for error_id in [-128, -1, 10000]:
        code, _ = curl("HEAD", TODOS + f"/{error_id}/categories")
        assert code == 200  # BUG: expected 404


def test_todos_id_categories_post_xml(client):
    code, content = curl(
        "POST",
        TODOS + "/1/categories",
        "xml",
        "json",
        "<category><id>1</id></category>",
    )
    assert code == 404 and sort_json(content) == sort_json(
        {"errorMessages": ["Could not find thing matching value for id"]}
    )  # BUG: expected 201, 404 not support xml


def test_todos_id_catrgories_id_notallow_get(client):
    code, _ = curl("GET", TODOS + "/1/categories/1")
    assert code == 404  # BUG: raise 404 should be 405


def test_todos_id_catrgories_id_notallow_post(client):
    code, _ = curl("POST", TODOS + "/1/categories/1")
    assert code == 404  # BUG: raise 404 should be 405


def test_todos_id_catrgories_id_notallow_head(client):
    code, _ = curl("HEAD", TODOS + "/1/categories/1")
    assert code == 404  # BUG: raise 404 should be 405


def test_todos_id_tasksof_post_xml(client):
    code, _ = curl(
        "POST",
        TODOS + "/2/tasksof",
        "xml",
        "json",
        data="<title>new title 2</title>",
    )
    assert code == 400  # BUG expected 201
    # {"errorMessages":
    # ["java.lang.IllegalStateException: Expected BEGIN_OBJECT but was STRING at line 1 column 1 path $"]}


def test_todos_id_tasksof_id_notallow_get(client):
    code, _ = curl("GET", TODOS + "/1/tasksof/1")
    assert code == 404  # BUG: raise 404 should be 405


def test_todos_id_tasksof_id_notallow_post(client):
    code, _ = curl("POST", TODOS + "/1/tasksof/1")
    assert code == 404  # BUG: raise 404 should be 405


def test_todos_id_tasksof_id_notallow_head(client):
    code, _ = curl("HEAD", TODOS + "/1/tasksof/1")
    assert code == 404  # BUG: raise 404 should be 405


################################################################
########################### PROJECT ############################
################################################################


def test_get_project_categories_wrong_id(client):
    code, content = curl("GET", PROJECTS + "/100/categories", "", "json")
    assert code == 200 and content  # BUG expected 404


def test_post_project_xml_xml(client):
    code, _ = curl("POST", PROJECTS, "xml", "xml", project_create_xml)
    assert code == 400  # BUG expected 201, not support xml


# def test_post_project_no_body_field_json(client):
#     code, content = curl("POST", PROJECTS + "/1", "json", "json", "{}")
#     assert code == 200 and "description" in content  # BUG: body error


def test_put_project_id(client):
    project_create_json["title"] = "new title"
    code, content = curl("put", PROJECTS + "/10", "", "json", json=project_create_json)
    assert code == 404  # BUG expected 200


def test_put_project(client):
    code, _ = curl("POST", PROJECTS + "/1", "", "xml", json=project_create_xml)
    assert code == 400  # BUG: expected 201, not support zml


def test_project_task_post_xml_xml(client):
    code, _ = curl("POST", PROJECTS + "/1/tasks", "xml", "xml", json=project_create_xml)
    assert code == 400  # BUG: expected 200, not support xml


def test_project_categories_xml_json(client):
    code, _ = curl(
        "POST", PROJECTS + "/1/categories", "xml", "json", json=project_create_xml
    )
    assert code == 400  # BUG: expected 200, not support xml


################################################################
######################## CATEGORIES ############################
################################################################


def test_get_categories_id6_todos(client):
    code, content = curl("GET", CATEGORIES + "/6" + "/todos", "", "json")
    assert code == 200  # BUG: expected 404, the parent node is null


def test_get_categories_id6_projects(client):
    code, content = curl("GET", CATEGORIES + "/6" + "/projects", "", "json")
    assert code == 200  # BUG: expected 404, the parent node does not exist.
