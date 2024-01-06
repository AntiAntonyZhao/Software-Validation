import json

import xmltodict

from ..config import TODOS
from ..utils import curl, sort_json
from .additional_test_data import *


def test_todos_post_json_json_good(client):
    code, content = curl("POST", TODOS, "json", "json", json.dumps(todos_post_data))
    assert code == 201 and sort_json(content) == sort_json(todos_post_response)


def test_todos_post_json_json_bad(client):
    code, content = curl("POST", TODOS, "json", "json", json.dumps(todos_post_data_bad))
    assert code == 400 and sort_json(content) == sort_json(todos_post_response)


def test_todos_id_tasksof_post_good(client):
    code, content = curl(
        "POST",
        TODOS + "/1/tasksof",
        "json",
        "xml",
        data=json.dumps({"title": "new title"}),
    )
    assert code == 201


def test_todos_id_tasksof_post_bad(client):
    code, _ = curl(
        "POST",
        TODOS + "/1/tasksof",
        "json",
        "xml",
        data=json.dumps({newtitle_bad}),
    )
    assert code == 201


def test_todos_post_json_xml_good(client):
    code, content = curl("POST", TODOS, "json", "xml", json.dumps(todos_post_data))
    assert code == 201 and sort_json(content) == sort_json(
        xmltodict.parse(todos_post_response_xml)
    )


def test_todos_post_json_xml_bad(client):
    code, content = curl("POST", TODOS, "json", "xml", json.dumps(todos_post_data))
    assert code == 201 and sort_json(content) == sort_json(
        xmltodict.parse(todos_post_response_xml_bad)
    )


def test_todos_id_tasksof_get_xml_good(client):
    # Test getting all project items related to a todo
    code, content = curl("GET", TODOS + "/1/tasksof", "", "xml")
    compare_content = xmltodict.parse(todos_id_tasksof_data_xml)
    assert code == 200 and sort_json(content) == sort_json(compare_content)


def test_todos_id_tasksof_get_xml_bad(client):
    code, content = curl("GET", TODOS + "/1/tasksof", "", "xml")
    compare_content = xmltodict.parse(todos_id_tasksof_data_xml_bad)
    assert code == 200 and sort_json(content) == sort_json(compare_content)
