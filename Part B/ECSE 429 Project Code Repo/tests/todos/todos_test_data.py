todos_get_response = {
    "todos": [
        {
            "id": "1",
            "title": "scan paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}],
            "categories": [{"id": "1"}],
        },
        {
            "id": "2",
            "title": "file paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}],
        },
    ]
}

todos_post_data = {"title": "Post new object"}
todos_post_data_xml = """<title>Post new object</title>"""

todos_post_response = {
    "id": "3",
    "title": "Post new object",
    "doneStatus": "false",
    "description": "",
}

todos_post_response_xml = """\
<todo>
    <doneStatus>false</doneStatus>
    <description/>
    <id>3</id>
    <title>Post new object</title>
</todo>"""


# /todos/:id
todos_id1_get_data = {
    "todos": [
        {
            "id": "1",
            "title": "scan paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}],
            "categories": [{"id": "1"}],
        }
    ]
}

todos_id2_get_data = {
    "todos": [
        {
            "id": "2",
            "title": "file paperwork",
            "doneStatus": "false",
            "description": "",
            "tasksof": [{"id": "1"}],
        }
    ]
}

todos_id1_get_data_xml = """\
<todos>
    <todo>
        <doneStatus>false</doneStatus>
        <description/>
        <tasksof>
            <id>1</id>
        </tasksof>
        <id>1</id>
        <categories>
            <id>1</id>
        </categories>
        <title>scan paperwork</title>
    </todo>
</todos>"""


todos_id2_get_data_xml = """\
<todos>
    <todo>
        <doneStatus>false</doneStatus>
        <description/>
        <tasksof>
            <id>1</id>
        </tasksof>
        <id>2</id>
        <title>file paperwork</title>
    </todo>
</todos>"""

todos_id_error_get_data = lambda x: {
    "errorMessages": [f"Could not find an instance with todos/{x}"]
}

todos_id_error_get_data_xml = (
    lambda x: f"""\
<errorMessages>
    <errorMessage>Could not find an instance with todos/{x}</errorMessage>
</errorMessages>
"""
)

todos_id_categories_get_data = {
    "categories": [
        {
            "id": "1",
            "title": "Office",
            "description": "",
        }
    ]
}

todos_id_categories_get_data_xml = """\
<categories>
    <category>
        <description/>
        <id>1</id>
        <title>Office</title>
    </category>
</categories>"""

todos_id_categories_error_get_data = lambda x: {
    "errorMessages": [f"Could not find any instances with todos/{x}/categories"]
}

todos_id_categories_error_get_data_xml = (
    lambda x: f"""\
<errorMessages>
    <errorMessage>Could not find any instances with todos/{x}/categories</errorMessage>
</errorMessages>
"""
)

todos_id_categories_id_error_delete_data = lambda x, y: {
    "errorMessages": [f"Could not find any instances with todos/{x}/categories/{y}"]
}

todos_id_categories_id_error_delete_data_xml = (
    lambda x, y: f"""\
<errorMessages>
    <errorMessage>Could not find any instances with todos/{x}/categories/{y}</errorMessage>
</errorMessages>
"""
)

todos_id_tasksof_post_data_xml = """\
<tasksof>
    <id>1</id>
</tasksof>
"""

todos_id_tasksof_data = {
    "projects": [
        {
            "id": "1",
            "title": "Office Work",
            "completed": "false",
            "active": "false",
            "description": "",
            "tasks": [{"id": "2"}, {"id": "1"}],
        }
    ]
}

todos_id_tasksof_data_xml = """\
<projects>
        <active>false</active>
        <description/>
        <id>1</id>
        <completed>false</completed>
        <title>Office Work</title>
        <tasks>
            <id>2</id>
        </tasks>
        <tasks>
            <id>1</id>
        </tasks>
</projects>"""

todos_id_put_data = {
    "title": "scan paperwork",
    "doneStatus": "false",
    "description": "",
}

todos_id_put_data_xml = """\
<todo>
    <doneStatus>false</doneStatus>
    <description/>
    <title>scan paperwork</title>
</todo>"""
