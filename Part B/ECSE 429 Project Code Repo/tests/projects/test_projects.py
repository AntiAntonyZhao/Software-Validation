import json

from ..config import PROJECTS
from ..utils import curl
from .project_test_data import *

f = open("ProjectExecution", "w")
f.write("Order:\n")
f.close()


def _write_id_sequence(ID):
    f = open("ProjectExecution", "a")
    f.write(f"{ID}\n")
    f.close()


# EDGE CASES
def test_get_project_id_not_exist(client):
    _write_id_sequence(0)
    code, _ = curl("GET", PROJECTS + "/100", "", "json")
    assert code == 404


def test_head_project_id_not_exist(client):
    _write_id_sequence(1)
    code, content = curl("HEAD", PROJECTS + "/100", "", "json")
    assert code == 404 and not content


def test_post_project_id_not_exist(client):
    _write_id_sequence(2)
    code, _ = curl("POST", PROJECTS + "/100", "", "json")
    assert code == 404


def test_post_project_bool_string(client):
    _write_id_sequence(3)
    code, content = curl(
        "POST", PROJECTS + "/1", "", "json", json=project_create_bool_as_string
    )
    assert (
        code == 400
        and "Failed Validation: completed should be BOOLEAN" in json.dumps(content)
    )


def test_put_project_id_not_exist(client):
    _write_id_sequence(4)
    code, _ = curl("PUT", PROJECTS + "/100", "", "json", json=project_create_json)
    assert code == 404


def test_put_project_no_body_field_json(client):
    _write_id_sequence(5)
    code, content = curl("PUT", PROJECTS + "/1", "", "json")
    assert code == 200 and content["title"] == ""


def test_put_project_no_body_field_json_null_entry(client):
    _write_id_sequence(6)
    project_create_tmp = project_create_json
    project_create_tmp["title"] = None
    code, content = curl("PUT", PROJECTS + "/1", "", "json", json=project_create_tmp)
    assert code == 200 and content["title"] == ""


def test_delete_project_exist_id(client):
    _write_id_sequence(7)
    code, _ = curl("DELETE", PROJECTS + "/1")
    assert code == 200


def test_delete_project_no_exist_id(client):
    _write_id_sequence(8)
    code, _ = curl("DELETE", PROJECTS + "/100")
    assert code == 404


def test_delete_project_task_wrong_ids(client):
    _write_id_sequence(9)
    code, _ = curl("DELETE", PROJECTS + "/100/tasks/100", "", "json")
    assert code == 404


def test_get_project_categories_wrong_id(client):
    _write_id_sequence(10)
    code, content = curl("GET", PROJECTS + "/100/categories", "", "json")
    assert code == 404 and not content  # BUG


def test_post_project_categories_error(client):
    _write_id_sequence(11)
    code, _ = curl("POST", PROJECTS + "/1/categories", "", "json", json={"id": "100"})
    assert code == 404


def test_post_project_categories_id_as_int(client):
    _write_id_sequence(12)
    code, _ = curl("POST", PROJECTS + "/100/categories", "", "json", json={"id": 100})
    assert code == 404


def test_delete_project_categories_wrong_ids(client):
    _write_id_sequence(13)
    code, _ = curl("DELETE", PROJECTS + "/100/categories/100")
    assert code == 404


# /projects
def test_get_projects(client):
    _write_id_sequence(14)
    code, content = curl("GET", PROJECTS, "", "json")
    assert code == 200
    assert "projects" in content


def test_get_projects_xml(client):
    _write_id_sequence(15)
    code, content = curl("GET", PROJECTS, "", "xml")
    assert code == 200
    assert "projects" in content


def test_post_project(client):
    _write_id_sequence(16)
    code, _ = curl("POST", PROJECTS, "", "")
    assert code == 201


def test_post_project_json_json(client):
    _write_id_sequence(17)
    code, _ = curl("POST", PROJECTS, "json", "json", json=project_create_json)
    assert code == 201


def test_post_project_xml_xml(client):
    _write_id_sequence(18)
    code, _ = curl("POST", PROJECTS, "xml", "xml", project_create_xml)
    assert code == 201  # BUG 400, not support xml


def test_head_projects(client):
    _write_id_sequence(19)
    code, content = curl("HEAD", PROJECTS, "", "json")
    assert code == 200 and not content


def test_not_allowed_put(client):
    _write_id_sequence(20)
    code, _ = curl("PUT", PROJECTS)
    assert code == 405


def test_not_allowed_delete(client):
    _write_id_sequence(21)
    code, _ = curl("DELETE", PROJECTS)
    assert code == 405


def test_not_allowed_path(client):
    _write_id_sequence(22)
    code, _ = curl("PATCH", PROJECTS)
    assert code == 405


# /projects/:id
def test_get_project_id_json(client):
    _write_id_sequence(23)
    code, content = curl("GET", PROJECTS + "/1", "", "json")
    assert code == 200 and "projects" in content


def test_get_project_id_xml(client):
    _write_id_sequence(24)
    code, content = curl("GET", PROJECTS + "/1", "", "xml")
    assert code == 200 and "projects" in content


# POST /projects/:id
def test_post_project_id_invalid(client):
    _write_id_sequence(25)
    code, _ = curl(
        "POST", PROJECTS + "/100", "json", "json", json.dumps(project_create_json)
    )
    assert code == 404


def test_post_project_no_body_field_json(client):
    _write_id_sequence(26)
    code, content = curl("POST", PROJECTS + "/1", "json", "json", "{}")
    assert code == 200 and "description" in content  # BUG: body error


# /projects/:id
def test_put_project_id_invalid(client):
    _write_id_sequence(27)
    code, _ = curl(
        "PUT", PROJECTS + "/100", "json", "json", json.dumps(project_create_json)
    )
    assert code == 404


def test_put_project_id(client):
    _write_id_sequence(28)
    project_create_json["title"] = "new title"
    code, content = curl("put", PROJECTS + "/10", "", "json", json=project_create_json)
    assert code == 200 and content["title"] == project_create_json["title"]  # BUG: 404


def test_head_project_id(client):
    _write_id_sequence(29)
    code, content = curl("head", PROJECTS + "/1", "", "json")
    assert code == 200 and not content


def test_post_project_id(client):
    _write_id_sequence(30)
    project_create_json["title"] = "new title"
    code, content = curl("post", PROJECTS + "/1", "", "json", json=project_create_json)
    assert code == 200 and content["title"] == project_create_json["title"]


def test_post_project_no_body_field_json_null_entry(client):
    _write_id_sequence(31)
    project_create_tmp = project_create_json
    project_create_tmp["title"] = None
    code, content = curl("post", PROJECTS + "/1", "", "json", json=project_create_tmp)
    assert (
        code == 200
        and "Office Work" in json.dumps(content)
        and "some description" in json.dumps(content)
    )


def test_delete_project_id(client):
    _write_id_sequence(32)
    code, content = curl("delete", PROJECTS + "/1")
    assert code == 200


# /projects/:id/tasks
def test_get_project_task(client):
    _write_id_sequence(33)
    code, content = curl("GET", PROJECTS + "/1/tasks", "", "json")
    assert code == 200 and "todos" in content


def test_head_project_task(client):
    _write_id_sequence(34)
    code, content = curl("head", PROJECTS + "/1/tasks", "", "json")
    assert code == 200 and not content


# POST /projects/:id/tasks
def test_post_project_task(client):
    _write_id_sequence(35)
    code, _ = curl("POST", PROJECTS + "/1/tasks", "json", "", json.dumps({"id": "1"}))
    assert code == 201


# DELETE /projects/:id/tasks/:id, Will delete according to the id of project or task
def test_delete_project_task(client):
    _write_id_sequence(36)
    code, _ = curl("DELETE", PROJECTS + "/1/tasks/1")
    assert code == 200


# /projects/:id/categories
def test_get_project_categories(client):
    _write_id_sequence(37)
    code, content = curl("GET", PROJECTS + "/1/categories", "", "json")
    assert code == 200
    assert "categories" in content


# POST /projects/:id/categories
def test_post_project_categories(client):
    _write_id_sequence(38)
    code, content = curl(
        "POST", PROJECTS + "/1/categories", "", "json", json={"id": "1"}
    )
    _, content = curl("get", PROJECTS + "/1/categories", "", "json")
    assert code == 201 and len(content["categories"]) == 1


# DELETE /projects/:id/categories/:id
def test_delete_project_categories(client):
    _write_id_sequence(39)
    code, _ = curl("DELETE", PROJECTS + "/1/categories/1")
    assert code == 404


def test_get_projects(client):
    _write_id_sequence(40)
    code, content = curl("GET", PROJECTS, "", "xml")
    assert code == 200 and "projects" in content


def test_post_project_id_not_exist_xml_xml(client):
    _write_id_sequence(41)
    code, content = curl(
        "POST", PROJECTS + "/100", "xml", "xml", json=project_create_xml_invalid_id
    )
    assert code == 404


def test_post_project_no_body_field_xml(client):
    _write_id_sequence(42)
    code, content = curl("POST", PROJECTS + "/1", "", "xml")
    assert code == 200


def test_put_project(client):
    _write_id_sequence(43)
    code, _ = curl("POST", PROJECTS + "/1", "", "xml", json=project_create_xml)
    assert code == 201  # BUG: not support xml


def test_project_task_post_xml_xml(client):
    _write_id_sequence(44)
    code, content = curl(
        "POST", PROJECTS + "/1/tasks", "xml", "xml", json=project_create_xml
    )
    assert code == 200 and content == ""  # BUG: not support xml


def test_project_categories_xml_json(client):
    _write_id_sequence(45)
    code, _ = curl(
        "POST", PROJECTS + "/1/categories", "xml", "json", json=project_create_xml
    )
    assert code == 200  # BUG: not support xml
