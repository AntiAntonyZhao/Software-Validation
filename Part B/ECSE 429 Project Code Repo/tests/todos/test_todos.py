import json

import xmltodict

from ..config import TODOS
from ..utils import curl, sort_json
from .todos_test_data import *


def test_todos_get_json(client):
    code, content = curl("GET", TODOS, "", "json")
    assert code == 200 and len(content["todos"]) == 2


def test_todos_get_xml(client):
    code, content = curl("GET", TODOS, "", "xml")
    assert code == 200 and len(content["todos"]["todo"]) == 2


# post
def test_todos_post_error(client):
    code, _ = curl("POST", TODOS, "", "")
    assert code == 400


def test_todos_xml_post_error(client):
    code, _ = curl("POST", TODOS, "", "")
    assert code == 400


# head
def test_todos_post_json_json(client):
    code, content = curl("POST", TODOS, "json", "json", json.dumps(todos_post_data))
    assert code == 201 and sort_json(content) == sort_json(todos_post_response)


def test_todos_post_json_xml(client):
    code, content = curl("POST", TODOS, "json", "xml", json.dumps(todos_post_data))
    assert code == 201 and sort_json(content) == sort_json(
        xmltodict.parse(todos_post_response_xml)
    )


def test_todos_xml_post_xml_json(client):
    code, content = curl("POST", TODOS, "xml", "json", todos_post_data_xml)
    assert code == 201 and sort_json(content) == sort_json(todos_post_response)
    # BUG: Not support xml
    # {"errorMessages":["java.lang.IllegalStateException: Expected BEGIN_OBJECT but was STRING at line 1 column 1 path $"]}


def test_todos_xml_post_xml_xml(client):
    code, content = curl("POST", TODOS, "xml", "xml", todos_post_data_xml)
    assert code == 201 and sort_json(content) == sort_json(
        xmltodict.parse(todos_post_response_xml)
    )
    # BUG: Not support xml
    # <errorMessages>
    # 	<errorMessage>java.lang.IllegalStateException: Expected BEGIN_OBJECT but was STRING at line 1 column 1 path $
    # 	</errorMessage>
    # </errorMessages>


def test_todos_notallow_put(client):
    code, _ = curl("PUT", TODOS)
    assert code == 405


def test_todos_notallow_delete(client):
    code, _ = curl("DELETE", TODOS)
    assert code == 405


def test_todos_notallow_patch(client):
    code, _ = curl("PATCH", TODOS)
    assert code == 405


# /todos/:id


def test_todos_id_get_json(client):
    code, content = curl("GET", TODOS + "/1", "", "json")
    assert code == 200 and sort_json(content) == sort_json(todos_id1_get_data)


def test_todos_id_get_json2(client):
    code, content = curl("GET", TODOS + "/2", "", "json")
    assert code == 200 and sort_json(content) == sort_json(todos_id2_get_data)


def test_todos_id_get_json_edge_case(client):
    for error_id in [-128, -1, 10000]:
        code, content = curl("GET", TODOS + f"/{error_id}", "", "json")
        assert code == 404 and sort_json(content) == sort_json(
            todos_id_error_get_data(error_id)
        )


def test_todos_id_get_xml(client):
    code, content = curl("GET", TODOS + "/1", "", "xml")
    compare_content = xmltodict.parse(todos_id1_get_data_xml)
    assert code == 200 and sort_json(content) == sort_json(compare_content)


def test_todos_id_get_xml2(client):
    code, content = curl("GET", TODOS + "/2", "", "xml")
    compare_content = xmltodict.parse(todos_id2_get_data_xml)
    assert code == 200 and sort_json(content) == sort_json(compare_content)


def test_todos_id_get_xml_edge_case(client):
    for error_id in [-128, -1, 10000]:
        code, content = curl("GET", TODOS + f"/{error_id}", "", "xml")
        assert code == 404 and sort_json(content) == sort_json(
            xmltodict.parse(todos_id_error_get_data_xml(error_id))
        )


def test_todos_id_head(client):
    code, content = curl("HEAD", TODOS + "/1")
    assert code == 200 and content == ""


def test_todos_id_put_json_json(client):
    # code, raw_content = curl("GET", TODOS + "/1", "", "json")
    # assert raw_content["todos"][0]["title"] == "scan paperwork" and raw_content["todos"][0]["description"] == "" \
    # and raw_content["todos"][0]["doneStatus"] == "false"
    # BUG: "false" should be False, json format wrong

    code, content = curl(
        "PUT", TODOS + "/1", "json", "json", json.dumps({"title": "Post new title 1"})
    )
    assert code == 200 and content["title"] == "Post new title 1"


def test_todos_id_put_json_json_title_desc(client):
    code, content = curl(
        "PUT",
        TODOS + "/1",
        "json",
        "json",
        json.dumps(
            {
                "title": "title3",
                "description": "Trying to create todo3 using POST",
                "doneStatus": True,
            }
        ),
    )
    assert (
        code == 200
        and content["title"] == "title3"
        and content["description"] == "Trying to create todo3 using POST"
        and content["doneStatus"] == "true"
    )


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
    assert (
        code == 200
        and content["title"] == "title3"
        and content["description"] == "Trying to create todo3 using POST"
        and content["doneStatus"] == "true"
    )
    # BUG: "true" should be True, json format wrong


def test_todos_id_put_json_xml(client):
    code, content = curl(
        "PUT", TODOS + "/1", "json", "xml", json.dumps(todos_id_put_data)
    )
    assert code == 200  # BUG 400


def test_todos_id_put_xml_json(client):
    code, content = curl("PUT", TODOS + "/1", "xml", "json", todos_id_put_data_xml)
    assert code == 200


def test_todos_id_put_xml_xml(client):
    code, content = curl("PUT", TODOS + "/1", "xml", "xml", todos_id_put_data_xml)
    assert code == 200


def test_todos_id_post_json_json(client):
    # code, raw_content = curl("GET", TODOS + "/1", "", "json")
    # assert raw_content["todos"][0]["title"] == "scan paperwork" and raw_content["todos"][0]["description"] == "" \
    # and raw_content["todos"][0]["doneStatus"] == "false"
    # BUG: "false" should be False, json format wrong

    code, content = curl(
        "post", TODOS + "/1", "json", "json", json.dumps({"title": "Post new title 1"})
    )
    assert code == 200 and content["title"] == "Post new title 1"


def test_todos_id_post_json_json_title_desc(client):
    code, content = curl(
        "post",
        TODOS + "/1",
        "json",
        "json",
        json.dumps(
            {
                "title": "title3",
                "description": "Trying to create todo3 using POST",
                "doneStatus": True,
            }
        ),
    )
    assert (
        code == 200
        and content["title"] == "title3"
        and content["description"] == "Trying to create todo3 using POST"
        and content["doneStatus"] == "true"
    )
    # BUG: "true" should be True, json format wrong


def test_todos_id_post_json_xml(client):
    code, content = curl(
        "post", TODOS + "/1", "json", "xml", json.dumps(todos_id_put_data)
    )
    assert code == 200  # BUG 400


def test_todos_id_post_xml_json(client):
    code, content = curl("post", TODOS + "/1", "xml", "json", todos_id_put_data_xml)
    assert code == 200
    # BUG: Not support xml


def test_todos_id_post_xml_xml(client):
    code, content = curl("post", TODOS + "/1", "xml", "xml", todos_id_put_data_xml)
    assert code == 200
    # BUG: Not support xml


def test_todos_id_post_error(client):
    # Test updating a todo with an invalid value
    indata = {
        "title": "title3",
        "description": "Trying to create todo3 using POST",
        "doneStatus": "true",
    }
    code, content = curl("post", TODOS + "/1", "", "json", json.dumps(indata))
    assert (
        code == 400
        and content["errorMessages"][0]
        == "Failed Validation: doneStatus should be BOOLEAN"
    )


def test_todos_id_put_error(client):
    # Test updating a todo with an invalid value
    indata = {
        "title": "title3",
        "description": "Trying to create todo3 using POST",
        "doneStatus": "true",
    }
    code, content = curl("PUT", TODOS + "/1", "", "json", json.dumps(indata))
    assert (
        code == 400
        and content["errorMessages"][0]
        == "Failed Validation: doneStatus should be BOOLEAN"
    )


def test_todos_id_delete(client):
    code, _ = curl("DELETE", TODOS + "/1")
    code1, content = curl("GET", TODOS + "/1", "", "json")
    assert code == 200 and code1 == 404


def test_todos_id_notallow(client):
    code, _ = curl("PATCH", TODOS + "/1")
    assert code == 405


# /todos/:id/categories/:id
# ["GET", "POST", "PUT", "DELETE", "HEAD", "PATCH"]
def test_todos_id_categories_get_json(client):
    code, content = curl("GET", TODOS + "/1/categories", "", "json")
    assert code == 200 and content == todos_id_categories_get_data


def test_todos_id_categories_get_json_edge_case(client):
    # BUG: continue return 200
    error_id = -129
    # for error_id in [-128, -1, 10000]:  # edge case
    code, content = curl("GET", TODOS + f"/{error_id}/categories", "", "json")
    assert code == 404 and content == todos_id_categories_error_get_data(error_id)
    # {
    #     "categories": [
    #         {
    #             "id": "1",
    #             "title": "Office",
    #             "description": ""
    #         }
    #     ]
    # }


def test_todos_id_categories_get_xml(client):
    code, content = curl("GET", TODOS + "/1/categories", "", "xml")
    compare_content = xmltodict.parse(todos_id_categories_get_data_xml)
    assert code == 200 and sort_json(content) == sort_json(compare_content)


def test_todos_id_categories_get_xml_edge_case(client):
    # BUG: continue return 200
    # for error_id in [-128, -1, 10000]:
    error_id = -129
    code, content = curl("GET", TODOS + f"/{error_id}/categories", "", "xml")
    compare_content = xmltodict.parse(todos_id_categories_error_get_data_xml(error_id))
    assert code == 404 and sort_json(content) == sort_json(compare_content)
    # <categories>
    #     <category>
    #         <description/>
    #         <id>1</id>
    #         <title>Office</title>
    #     </category>
    # </categories>


def test_todos_id_categories_head(client):
    code, _ = curl("HEAD", TODOS + "/1/categories")
    assert code == 200


def test_todos_id_categories_head2(client):
    code, _ = curl("HEAD", TODOS + "/2/categories")
    assert code == 200


def test_todos_id_categories_head_edge_case(client):
    for error_id in [-128, -1, 10000]:
        code, _ = curl("HEAD", TODOS + f"/{error_id}/categories")
        assert code == 404  # BUG: should be 404, always return following content


def test_todos_id_categories_post_json_json(client):
    code, content = curl(
        "POST",
        TODOS + "/1/categories",
        "json",
        "",
        json.dumps({"id": "1"}),
    )
    # assert code == 201 and content == "" # TODO: should not be allowd???

    code, content = curl(
        "POST",
        TODOS + "/1/categories",
        "json",
        "json",
        json.dumps({"title": "new cate title json"}),
    )
    assert code == 201 and content["title"] == "new cate title json"


def test_todos_id_categories_post_xml(client):
    code, content = curl(
        "POST", TODOS + "/1/categories", "xml", "", "<category><id>1</id></category>"
    )
    assert code == 201 and content == ""  # BUG: 404 not support xml


def test_todos_id_categories_post_xml_json(client):
    code, content = curl(
        "POST",
        TODOS + "/1/categories",
        "xml",
        "json",
        "<category><title>new cate title xml</title></category>",
    )
    assert code == 201 and content["title"] == "new cate title xml"


def test_todos_id_categories_notallow_put(client):
    code, _ = curl("PUT", TODOS + "/1/categories")
    assert code == 405


def test_todos_id_categories_notallow_delete(client):
    code, _ = curl("DELETE", TODOS + "/1/categories")
    assert code == 405


def test_todos_id_categories_notallow_path(client):
    code, _ = curl("PATCH", TODOS + "/1/categories")
    assert code == 405


# /todos/:id/categories/:id
def test_todos_id_categories_id_delete(client):
    # Test deleting an existing relationship
    code, _ = curl("DELETE", TODOS + "/1/categories/1")
    assert code == 200

    # Test deleting a non-existing relationship
    code, content = curl("DELETE", TODOS + "/1/categories/1")
    assert code == 404

    # Test deleting a relationship with an invalid todo ID
    code, content = curl("DELETE", TODOS + "/-1/categories/1", "", "json")
    assert code == 404 and sort_json(content) == sort_json(
        todos_id_categories_id_error_delete_data(-1, 1)
    )

    # Test deleting a relationship with an invalid category ID
    code, content = curl("DELETE", TODOS + "/1/categories/-1", "", "xml")
    assert code == 404
    compare_content = xmltodict.parse(
        todos_id_categories_id_error_delete_data_xml(1, -1)
    )
    assert sort_json(content) == sort_json(compare_content)


def test_todos_id_catrgories_id_notallow_get(client):
    # BUG: raise 404 should be 405,  or not consistany with other methods
    code, _ = curl("GET", TODOS + "/1/categories/1")
    assert code == 405


def test_todos_id_catrgories_id_notallow_post(client):
    code, _ = curl("POST", TODOS + "/1/categories/1")
    assert code == 405


def test_todos_id_catrgories_id_notallow_put(client):
    code, _ = curl("PUT", TODOS + "/1/categories/1")
    assert code == 405


def test_todos_id_catrgories_id_notallow_head(client):
    code, _ = curl("HEAD", TODOS + "/1/categories/1")
    assert code == 405  # BUG: raise 404 should be 405


def test_todos_id_catrgories_id_notallow_patch(client):
    code, _ = curl("PATCH", TODOS + "/1/categories/1")
    assert code == 405


def test_todos_id_tasksof_get_json(client):
    # Test getting all project items related to a todo
    code, content = curl("GET", TODOS + "/1/tasksof", "", "json")
    assert code == 200 and sort_json(content) == sort_json(todos_id_tasksof_data)


def test_todos_id_tasksof_get_xml(client):
    # Test getting all project items related to a todo
    code, content = curl("GET", TODOS + "/1/tasksof", "", "xml")
    compare_content = xmltodict.parse(todos_id_tasksof_data_xml)
    assert code == 200 and sort_json(content) == sort_json(compare_content)


def test_todos_id_tasksof_head(client):
    # Test getting headers for all project items related to a todo
    code, _ = curl("HEAD", TODOS + "/1/tasksof")
    assert code == 200


def test_todos_id_tasksof_post(client):
    # Test creating a relationship between a todo and a project
    code, _ = curl("POST", TODOS + "/1/tasksof")
    assert code == 201

    code, _ = curl(
        "POST", TODOS + "/1/tasksof", "json", "", data=json.dumps({"id": "1"})
    )
    code1, _ = curl(
        "POST",
        TODOS + "/1/tasksof",
        "json",
        "xml",
        data=json.dumps({"title": "new title"}),
    )
    assert code == 201 and code1 == 201


def test_todos_id_tasksof_post_xml(client):
    code, _ = curl(
        "POST",
        TODOS + "/2/tasksof",
        "xml",
        "json",
        data="<title>new title 2</title>",
    )
    assert code == 201  # BUG 404
    # {"errorMessages":
    # ["java.lang.IllegalStateException: Expected BEGIN_OBJECT but was STRING at line 1 column 1 path $"]}


def test_todos_id_tasksof_notallow_put(client):
    # Test that other methods are not allowed for /todos/:id/tasksof
    code, _ = curl("PUT", TODOS + "/1/tasksof")
    assert code == 405


def test_todos_id_tasksof_notallow_patch(client):
    code, _ = curl("PATCH", TODOS + "/1/tasksof")
    assert code == 405


def test_todos_id_tasksof_id_delete(client):
    # Test deleting a relationship between a todo and a project
    code, _ = curl("DELETE", TODOS + "/1/tasksof/1")
    code1, _ = curl("DELETE", TODOS + "/1/tasksof/1")
    assert code == 200 and code1 == 404


def test_todos_id_tasksof_id_notallow_get(client):
    # Test that other methods are not allowed for /todos/:id/tasksof/:id
    code, _ = curl("GET", TODOS + "/1/tasksof/1")
    assert code == 405  # BUG: raise 404 should be 405


def test_todos_id_tasksof_id_notallow_post(client):
    code, _ = curl("POST", TODOS + "/1/tasksof/1")
    assert code == 405


def test_todos_id_tasksof_id_notallow_put(client):
    code, _ = curl("PUT", TODOS + "/1/tasksof/1")
    assert code == 405


def test_todos_id_tasksof_id_notallow_head(client):
    code, _ = curl("HEAD", TODOS + "/1/tasksof/1")
    assert code == 405


def test_todos_id_tasksof_id_notallow_patch(client):
    code, _ = curl("PATCH", TODOS + "/1/tasksof/1")
    assert code == 405
