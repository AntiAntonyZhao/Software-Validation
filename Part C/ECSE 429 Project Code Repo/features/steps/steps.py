import json

from behave import given, then, when
from behave.runner import Context

from tests.config import *
from tests.utils import curl

#### Helper function ####


def process_bool(s):
    return "true" if s == "True" else "false"


def to_bool(s):
    return s == "True"


def json_to_bool(s):
    return s == "true"


#########################
@given(
    "A user adds a task with title {task_title}, description {task_description} and done status {task_done_status} to the project"
)
@when(
    "A user adds a task with title {task_title}, description {task_description} and done status {task_done_status} to the project"
)
def step_impl(
    context: Context, task_title: str, task_description: str, task_done_status: str
):
    """Creates a new todo item and links it to a project."""
    project = {"id": context.project["id"]}

    # create the todo
    create_todo = curl(
        "POST",
        TODOS,
        "json",
        "json",
        json.dumps(
            {
                "title": task_title,
                "description": task_description,
                "doneStatus": to_bool(task_done_status),
            }
        ),
    )
    todo_res = create_todo[1]
    todos = curl("GET", TODOS, response_style="json")[1]["todos"]

    # create the link with course to do list
    todo_project_relationship = curl(
        "POST",
        TODOS_ID_TASKSOF.format(todo_res["id"]),
        data_style="json",
        response_style="json",
        data=json.dumps(project),
    )
    todo = curl("GET", TODOS_ID.format(todo_res["id"]), response_style="json")[1][
        "todos"
    ][0]
    context.task = todo

    assert (
        create_todo[0] == 201
        and todo_project_relationship[0] == 201
        and todo_res in todos
    )


@then("This task should be contained in the course to do list")
def step_impl(context):
    """Check if the task is contained in the course to do list."""
    context.project = curl(
        "GET",
        PROJECTS_ID.format(context.project["id"]),
        response_style="json",
    )[1]["projects"][0]
    compare = [
        True if task["id"] == context.task["id"] else False
        for task in context.project["tasks"]
    ]
    assert any(compare)


@then("The project should be associated to the task")
def step_impl(context):
    """Asserts that the project is associated with the task."""
    assert context.task["tasksof"][0]["id"] == context.project["id"]


@when(
    "A user adds a task that does not exist with title {task_title}, description {task_description} and done status {task_done_status} to the project"
)
def step_impl(context, task_title, task_description, task_done_status):
    """Adds a task to the project with the given title, description, and done status."""
    task = {
        "id": "12345",
        "title": task_title,
        "description": task_description,
        "doneStatus": to_bool(task_done_status),
    }
    project = {"id": context.project["id"]}

    # create the link with course to do list
    todo_project_relationship = curl(
        "POST",
        TODOS_ID_TASKSOF.format(task["id"]),
        data_style="json",
        response_style="json",
        data=json.dumps(project),
    )
    context.error_request = todo_project_relationship[1]
    assert todo_project_relationship[0] == 404


@then("We should receive an error message")
def step_impl(context):
    """Asserts that the 'errorMessages' key is present in the context's error_request dictionary."""
    assert "errorMessages" in context.error_request


@then("The project with {project_title} should not be deleted")
def step_impl(context, project_title):
    """Check if a project with the given title exists in the list of projects."""
    response = curl("GET", PROJECTS, response_style="json")
    projects = response[1]["projects"]

    assert any(project_title == project["title"] for project in projects)


@when("A user delete the project with title {project_title}")
def step_impl(context, project_title):
    """A user delete the project with title {project_title}"""
    projects = curl("GET", PROJECTS, "", "json")[1]["projects"]
    for project in projects:
        if project_title == project["title"]:
            # delete this project
            deleted_project = curl(
                "GET", PROJECTS_ID.format(project["id"]), response_style="json"
            )[1]["projects"][0]
            code, _ = curl(
                "DELETE",
                PROJECTS_ID.format(project["id"]),
                response_style="json",
            )
            context.deleted_project = deleted_project
            context.projects = projects
            assert code == 200


@then("The project object is deleted")
def step_impl(context):
    """
    Asserts that the project object is deleted by checking if the deleted project is not in the list of projects
    and the length of the projects list is reduced by 1.
    """
    projects = curl("GET", PROJECTS, "", "json")[1]["projects"]
    assert (
        context.deleted_project not in projects
        and len(projects) == len(context.projects) - 1
    )


@given(
    "A task with title {task_title}, description {task_description} and done status {task_done_status} linked to category with title {category_title} and description {category_description}"
)
def create_task_linked_to_category(
    context: Context,
    task_title: str,
    task_description: str,
    task_done_status: str,
    category_title: str,
    category_description: str,
) -> None:
    """Creates a task with the given title, description, and done status, and links it to a category with the given title and description."""
    # Create task
    create_todo = curl(
        "POST",
        TODOS,
        data_style="json",
        response_style="json",
        json={
            "title": str(task_title),
            "description": str(task_description),
            "doneStatus": not task_done_status == "False",
        },
    )
    todo_res = create_todo[1]
    todos = curl("GET", TODOS, response_style="json")[1]["todos"]
    context.task_id = todo_res["id"]
    context.task_title = todo_res["title"]
    context.task = todo_res

    # Create old category
    create_category = curl(
        "POST",
        CATEGORIES,
        data_style="json",
        response_style="json",
        json={"title": str(category_title), "description": str(category_description)},
    )
    category_res = create_category[1]
    categories = curl("GET", CATEGORIES, response_style="json")[1]["categories"]
    context.old_category_id = category_res["id"]

    # Link them
    task = {"id": context.task_id}
    code, _ = curl(
        "POST",
        CATEGORIES + "/%d/todos" % int(context.old_category_id),
        data_style="json",
        response_style="json",
        json=task,
    )

    assert (
        create_todo[0] == 201
        and todo_res in todos
        and create_category[0] == 201
        and category_res in categories
        and code == 201
    )


@when("A user unlinks a task from old category")
def step_impl(context):
    """Unlinks a task from an old category."""
    task = {"id": context.task_id}
    code, _ = curl(
        "DELETE",
        CATEGORIES
        + "/%d/todos/%d" % (int(context.old_category_id), int(context.task_id)),
        data_style="json",
        response_style="json",
        json=task,
    )
    assert code == 200


@then("The category should not be able to be unlinked")
def step_impl(context):
    """Verify that the category cannot be unlinked by sending a DELETE request to the API endpoint."""
    code, _ = curl(
        "DELETE",
        CATEGORIES + "/%d/todos/%d" % (int(context.category_id), int(context.task_id)),
        response_style="json",
    )
    assert code == 404


@given(
    "An existing project with title {project_title}, description {project_description}, complete status {project_completed} and active status {project_active}"
)
@given(
    "A user creates a project with title {project_title}, description {project_description}, complete status {project_completed} and active status {project_active}"
)
@when(
    "A user creates a project with title {project_title}, description {project_description}, complete status {project_completed} and active status {project_active}"
)
def step_impl(
    context: Context,
    project_title: str,
    project_description: str,
    project_completed: str,
    project_active: str,
) -> None:
    """
    Create a project with the given title, description, complete status, and active status.
    If the project already exists, use the existing project with the same title and description.
    """
    project = {
        "completed": to_bool(project_completed),
        "active": to_bool(project_active),
        "title": project_title,
        "description": project_description,
    }
    status_code, content = curl(
        "POST", PROJECTS, data_style="json", response_style="json", json=project
    )
    project_res = content
    status_code, content = curl("GET", PROJECTS, response_style="json")
    projects = content["projects"]
    # context.projects = projects
    context.project = project_res
    assert status_code == 200 and project_res in projects


@then(
    "The projects should contain a project with title {project_title}, description {project_description}, complete status {project_completed} and active status {project_active}"
)
def step_impl(
    context: Context,
    project_title: str,
    project_description: str,
    project_completed: str,
    project_active: str,
) -> None:
    """Verify that the list of projects contains a project with the specified title, description, completed status, and active status."""
    status_code, content = curl("GET", PROJECTS, response_style="json")
    projects = content["projects"]
    compare = [
        True
        if project_title == project["title"]
        and project_description == project["description"]
        and to_bool(project_active) == json_to_bool(project["active"])
        and to_bool(project_completed) == json_to_bool(project["completed"])
        else False
        for project in projects
    ]
    assert status_code == 200 and any(compare)


@then(
    "The projects should not contain a project with title {project_title}, description {project_description}, complete status {project_completed} and active status {project_active}"
)
def step_impl(
    context: Context,
    project_title: str,
    project_description: str,
    project_completed: str,
    project_active: str,
) -> None:
    """Asserts that there is no project in the list of projects with the given title, description, completed status, and active status."""
    status_code, content = curl("GET", PROJECTS, response_style="json")
    projects = content["projects"]
    for project in projects:
        assert status_code == 200 and not (
            project_title == project["title"]
            and project_description == project["description"]
            and to_bool(project_active) == json_to_bool(project["active"])
            and to_bool(project_completed) == json_to_bool(project["completed"])
        )


@given(
    "There is not a project with title {project_title}, description {project_description}, complete status {project_completed} and active status {project_active}"
)
def step_impl(
    context: Context,
    project_title,
    project_description,
    project_completed,
    project_active,
):
    """
    Given a project with title, description, complete status and active status does not exist,
    this function checks if the project exists in the system by sending a GET request to the server.
    If the project exists, it asserts that the project does not have the same title, description, complete status and active status as the given project.
    """
    status_code, content = curl("GET", PROJECTS, response_style="json")
    projects = content["projects"]
    # context.projects = projects
    for project in projects:
        assert status_code == 200 and not (
            project_title == project["title"]
            and project_description == project["description"]
            and to_bool(project_active) == json_to_bool(project["active"])
            and to_bool(project_completed) == json_to_bool(project["completed"])
        )


@when("A user creates a project with id {id}")
def step_impl(context: Context, id):
    """Sends a POST request to create a project with the given id and stores the response in the context."""
    status_code, content = curl(
        "POST",
        PROJECTS,
        data_style="json",
        response_style="json",
        json={"id": id},
    )
    project_res = content
    assert status_code == 400 and "errorMessages" in project_res


@given(
    "A task with title {task_title}, description {task_description} and done status {task_done_status}"
)
def step_impl(context, task_title, task_description, task_done_status):
    """Create a task with given title, description and done status"""

    code, todo_res = curl(
        "POST",
        TODOS,
        data_style="json",
        response_style="json",
        json={
            "title": str(task_title),
            "description": str(task_description),
            "doneStatus": bool(task_done_status),
        },
    )
    todos = curl("GET", TODOS, response_style="json")[1]["todos"]
    context.task_id = todo_res["id"]
    context.task_title = todo_res["title"]
    context.task = todo_res
    assert code == 201 and todo_res in todos


@when("A user marks the task {task_title} as done")
def step_impl(context, task_title):
    """Marks a task as done."""
    task_update = {"title": str(task_title), "doneStatus": True}
    code, _ = curl(
        "PUT",
        TODOS_ID.format(context.task_id),
        data_style="json",
        response_style="json",
        json=task_update,
    )
    assert code == 200


@when("A user marks the task {task_title} as not done")
def step_impl(context, task_title):
    """Marks a task as not done."""
    task_update = {"title": str(task_title), "doneStatus": False}
    code, _ = curl(
        "PUT",
        TODOS_ID.format(context.task_id),
        data_style="json",
        response_style="json",
        json=task_update,
    )
    assert code == 200


@then("The task should have a a doneStatus of {task_done_status}")
def step_impl(context, task_done_status):
    """Asserts that the doneStatus of the task is equal to the given task_done_status."""
    response = curl(
        "GET",
        TODOS_ID.format(context.task_id),
        response_style="json",
    )
    todo = response[1]["todos"][0]
    assert (
        response[0] == 200
        and str(task_done_status).casefold() == str(todo["doneStatus"]).casefold()
    )


@when("A user marks the wrong task {wrong_task_id} as done")
def step_impl(context, wrong_task_id):
    """Mark the wrong task as done."""
    task_update = {"doneStatus": True}
    response = curl(
        "PUT",
        TODOS_ID.format(wrong_task_id),
        data_style="json",
        response_style="json",
        json=task_update,
    )
    context.status_code = 404


@when(
    "A user selects the {wrong_task_id} to change the description to {new_task_description}"
)
def step_impl(context, wrong_task_id, new_task_description):
    """Change the description of a task with the wrong ID to a new description."""
    task_update = {"description": new_task_description}
    response = curl(
        "PUT",
        TODOS_ID.format(wrong_task_id),
        data_style="json",
        response_style="json",
        json=task_update,
    )
    context.status_code = 404


@then("There should be a 404 NotFound error")
def step_impl(context):
    """Asserts that the status code in the context is 404."""
    assert context.status_code == 404


@given(
    "A task with title {project_title}, project status {project_completed} and project description {project_description}"
)
def step_impl(context, project_title, project_completed, project_description):
    """Create a project with the given title, completion status, and description."""

    create_project_data = {
        "title": str(project_title),
        "description": str(project_description),
        "completed": bool(project_completed),
    }
    status_code, project_res = curl(
        "POST", PROJECTS, json=create_project_data, response_style="json"
    )
    projects = [] if status_code == 200 else project_res
    context.project_id = project_res["id"]
    context.project_title = project_res["title"]
    context.project = project_res
    print(status_code, project_res, projects)
    assert status_code == 201 and sorted(project_res) == sorted(projects)


@given(
    "A task with description {task_description}, task {task_title}, and done status {task_done_status} linked to project with title {project_title}, done status {project_completed}, active status {project_active} and description {project_description}"
)
def step_impl(
    context,
    task_title,
    task_description,
    task_done_status,
    project_title,
    project_completed,
    project_active,
    project_description,
):
    """Create a task and a project, link them together and store their ids in the context"""
    # Create task
    create_todo_data = {
        "title": str(task_title),
        "description": str(task_description),
        "doneStatus": bool(task_done_status),
    }
    status_code, todo_res = curl(
        "POST", TODOS, json=create_todo_data, response_style="json"
    )
    context.task_id = todo_res["id"]
    context.task_title = todo_res["title"]
    context.task = todo_res
    assert status_code == 201

    # Create project
    create_project_data = {
        "title": str(project_title),
        "description": str(project_description),
        "completed": bool(project_completed),
        "active": bool(project_active),
    }
    status_code, project_res = curl(
        "POST", PROJECTS, json=create_project_data, response_style="json"
    )
    # projects = [] if status_code == 200 else project_res
    context.project_id = project_res["id"]
    context.project_title = project_res["title"]
    context.project = project_res
    assert status_code == 201  # and project_res == projects

    # Link them
    task = {"id": context.task_id}
    link_task_data = json.dumps(task)
    status_code, _ = curl(
        "POST",
        f"{PROJECTS}/{int(context.project_id)}/tasks",
        data=link_task_data,
        response_style="json",
    )
    # print("link", status_code)
    assert status_code == 201
    context.old_project_id = context.project_id


@given(
    "A complete task with title {task_title}, description {task_description} linked to project"
)
def step_impl(context, task_title, task_description):
    """Create a complete task with given title and description and link it to a project."""

    # Create task
    create_todo_data = {
        "title": str(task_title),
        "description": str(task_description),
        "doneStatus": True,
    }
    status_code, todo_res = curl(
        "POST", TODOS, json=create_todo_data, response_style="json"
    )
    todos_data = {"todos": []}
    if status_code == 200:
        todos_data = {"todos": todo_res}
    todos = todos_data["todos"]
    context.complete_task_id = todo_res["id"]
    context.complete_task_title = todo_res["title"]
    context.complete_task = todo_res
    assert status_code == 201  # and todo_res in todos

    # Link to project
    task = {"id": context.complete_task_id}
    link_task_data = json.dumps(task)
    status_code, _ = curl(
        "POST",
        f"{PROJECTS}/{int(context.old_project_id)}/tasks",
        data=link_task_data,
        response_style="json",
    )
    assert status_code == 201


@then("Only incomplete task for class should be returned")
def step_impl(context):
    """Asserts that only incomplete tasks for a class are returned"""

    status_code, r = curl(
        "GET",
        f"{PROJECTS}/{int(context.old_project_id)}/tasks?doneStatus=false",
        response_style="json",
    )
    print("incomplete", r, "status code", status_code)

    assert status_code == 200
    assert len(r["todos"]) > 0
    assert r["todos"][0]["doneStatus"] == "false"


@then("No tasks for class should be returned")
def step_impl(context):
    """Asserts that no tasks are returned for a given project ID"""
    status_code, r = curl(
        "GET",
        f"{PROJECTS}/{int(context.old_project_id)}/tasks?doneStatus=false",
        response_style="json",
    )
    assert status_code == 200 and len(r["todos"]) == 0


@then("Tasks for class should be returned")
def step_impl(context):
    """Asserts that tasks for a class are returned."""
    status_code, r = curl(
        "GET",
        f"{PROJECTS}/{int(context.old_project_id)}/tasks",
        response_style="json",
    )
    assert status_code == 200 and len(r["todos"]) != 0


@given("A complete task with title {task_title}, description {task_description}")
def create_complete_task(context, task_title, task_description):
    """Create a complete task with given title and description"""

    data = {
        "title": str(task_title),
        "description": str(task_description),
        "doneStatus": True,
    }
    status_code, todo_res = curl("POST", TODOS, "json", "json", json=data)
    status_code, content = curl("GET", TODOS, "", "json")
    todos = content["todos"]
    context.complete_task_id = todo_res["id"]
    context.complete_task_title = todo_res["title"]
    context.complete_task = todo_res

    # Link to category
    task = {"id": context.complete_task_id}
    url = CATEGORIES + "/%d/todos" % int(context.old_category_id)
    status_code, _ = curl("POST", url, "json", "json", json=task)
    # print("link", status_code, todo_res, todos)
    assert status_code == 201 and todo_res in todos


@then("Only incomplete task for category should be returned")
def check_incomplete_task(context):
    """Check that only incomplete tasks for a category are returned"""
    url = CATEGORIES + "/%d/todos" % int(context.old_category_id)
    params = {"doneStatus": False}
    status_code, content = curl("GET", url, response_style="json", json=params)
    print(content)
    assert status_code == 200 and all(
        todo["doneStatus"] == "false" for todo in content["todos"]
    )


@then("No Tasks for category should be returned")
def check_no_task(context):
    """Check if no tasks are returned for a given category"""
    url = CATEGORIES + "/%d/todos" % int(context.old_category_id)
    params = {"doneStatus": False}
    status_code, content = curl("GET", url, params=params, response_style="json")
    assert status_code == 200 and len(content["todos"]) == 0


@then("Tasks for category should be returned")
def check_task(context):
    """Check if tasks for a category are returned"""
    url = CATEGORIES + "/%d/todos" % int(context.old_category_id)
    status_code, content = curl("GET", url, response_style="json")
    assert status_code == 200 and len(content["todos"]) != 0


@when("A user removes that task from the course to do list")
def step_impl(context: Context):
    """Remove a task from the course to do list"""
    # delete this todo
    response = curl("GET", TODOS_ID.format(context.task["id"]), response_style="json")
    deleted_todo = response[1]["todos"][0]
    response = curl(
        "DELETE", TODOS_ID.format(context.task["id"]), response_style="json"
    )
    new_todos = curl("GET", TODOS, response_style="json")[1]["todos"]
    context.deleted_task = deleted_todo
    assert response[0] == 200 and deleted_todo not in new_todos


@then("The task should no longer be contained in the todo list")
def step_impl(context: Context):
    """Asserts that the task is no longer in the todo list."""
    context.project = curl(
        "GET", PROJECTS_ID.format(context.project["id"]), response_style="json"
    )[1]["projects"][0]
    assert context.project.get("tasks") == None


@when("A user removes a nonexisting task from the course to do list")
def step_impl(context: Context):
    """Remove a non-existing task from the course to do list."""
    not_existing_task = {
        "id": "12345",
        "title": "random",
        "description": "not existing",
        "doneStatus": False,
    }

    # create the link with course to do list
    response = curl(
        "DELETE", TODOS_ID.format(not_existing_task["id"]), response_style="json"
    )
    context.error_request = response[1]
    assert response[0] == 404


# Given steps
@given(
    "An non existing project with title {project_title}, description {project_description}, complete status {project_completed} and active status {project_active}"
)
def step_impl(
    context: Context,
    project_title: str,
    project_description: str,
    project_completed: str,
    project_active: str,
):
    """Set up a project and check if it already exists."""
    # Set up the project
    context.project = {
        "id": 200,
        "completed": to_bool(project_completed),
        "active": to_bool(project_active),
        "title": project_title,
        "description": project_description,
    }
    # Check if the project already exists
    code, projects = curl("GET", PROJECTS, "", "json")
    for project in projects["projects"]:
        assert not (
            project_title == project["title"]
            and project_description == project["description"]
            and to_bool(project_active) == json_to_bool(project["active"])
            and to_bool(project_completed) == json_to_bool(project["completed"])
        )


# When steps
@when("A user removes that project")
def step_impl(context: Context):
    """Deletes a project and verifies that it has been deleted."""

    # Get the list of projects
    projects = curl("GET", PROJECTS, "", "json")[1]["projects"]
    # Set up the project to be deleted
    project = {
        "id": context.project["id"],
        "title": context.project["title"],
        "description": context.project["description"],
        "active": process_bool(context.project["active"]),
        "completed": process_bool(context.project["completed"]),
    }
    # Delete the project
    deleted_project = curl(
        "GET", PROJECTS_ID.format(project["id"]), response_style="json"
    )[1]["projects"][0]
    code, _ = curl("DELETE", PROJECTS_ID.format(project["id"]), response_style="json")
    new_projects = curl("GET", PROJECTS, "", "json")[1]["projects"]
    assert (
        code == 200
        and deleted_project not in new_projects
        and len(new_projects) == len(projects) - 1
    )


@when("A user removes a non existing project")
def step_impl(context: Context):
    """Deletes a project and verifies that it was deleted successfully."""

    # Get the list of projects
    projects = curl("GET", PROJECTS, "", "json")[1]["projects"]
    # Set up the project to be deleted
    project = context.project
    # Delete the project
    r = curl(
        "DELETE",
        PROJECTS_ID.format(project["id"]),
        response_style="json",
    )
    new_projects = curl("GET", PROJECTS, "", "json")[1]["projects"]
    assert (
        project not in projects and r[0] == 404 and len(new_projects) == len(projects)
    )


@when("A user changes the description to {new_task_description}")
def step_impl(context, new_task_description):
    """Update the task description with the given new_task_description."""

    # Update the task description
    task_update = {"title": context.task_title, "description": new_task_description}
    context.new_task_description = new_task_description
    status_code, _ = curl(
        "PUT",
        TODOS_ID.format(context.task_id),
        data_style="json",
        response_style="json",
        json=task_update,
    )
    assert status_code == 200


@when("A user removes the task description")
def step_impl(context):
    """Updates the task description to an empty string."""

    # Remove the task description
    task_update = {"title": context.task_title, "description": ""}
    context.new_task_description = ""
    status_code, _ = curl(
        "PUT",
        TODOS_ID.format(context.task_id),
        data_style="json",
        response_style="json",
        json=task_update,
    )
    assert status_code == 200


@when("A user links a task to a category")
def step_impl(context):
    """Link a task to a category"""

    task = {"id": context.task_id}
    r = curl(
        "POST",
        f"{CATEGORIES}/{int(context.category_id)}/todos",
        data_style="json",
        response_style="json",
        json=task,
    )
    assert r[0] == 201


@when("A user links the category to the given task")
def step_impl(context):
    """Link a category to a task"""

    # Link a category to a task
    category = {"id": context.category_id}
    r = curl(
        "POST",
        f"{TODOS}/{int(context.task_id)}/categories",
        data_style="json",
        response_style="json",
        json=category,
    )
    assert r[0] == 201


@when("A user links an invalid category with {wrong_category_id} to the given task")
def step_impl(context, wrong_category_id):
    """Link an invalid category to a task and assert that the response status code is 404"""
    category = {"id": wrong_category_id}
    r = curl(
        "POST",
        f"{TODOS}/{int(context.task_id)}/categories",
        data_style="json",
        response_style="json",
        json=category,
    )
    context.r = r
    assert r[0] == 404


# Then steps
@then("The projects should not be contained")
def step_impl(context: Context):
    """Check if the project has been deleted"""

    projects = curl("GET", PROJECTS, "", "json")[1]["projects"]
    deleted_project = context.project
    for project in projects:
        assert not (
            deleted_project["title"] == project["title"]
            and deleted_project["description"] == project["description"]
            and to_bool(deleted_project["active"]) == json_to_bool(project["active"])
            and to_bool(deleted_project["completed"])
            == json_to_bool(project["completed"])
        )


@then("The task description should be changed")
def step_impl(context):
    """Check if the task description has been changed."""

    # Check if the task description has been changed
    status_code, content = curl(
        "GET",
        TODOS_ID.format(context.task_id),
        data_style="json",
        response_style="json",
    )
    todo = content["todos"][0]
    assert status_code == 200 and str(context.new_task_description) == str(
        todo["description"]
    )


@then("The task description should be empty")
def step_impl(context):
    """Check if the task description is empty"""

    # Check if the task description is empty
    status_code, content = curl(
        "GET",
        TODOS_ID.format(context.task_id),
        data_style="json",
        response_style="json",
    )
    todo = content["todos"][0]
    assert status_code == 200 and str(context.new_task_description) == str(
        todo["description"]
    )


@then("The task should be linked to the category")
def step_impl(context):
    """Check if the task is linked to the category"""

    # Check if the task is linked to the category
    category = {"id": context.category_id}
    status_code, content = curl(
        "GET",
        f"{TODOS}/{int(context.task_id)}",
        response_style="json",
    )
    modified_todo_json = content["todos"][0]
    print(content)
    print(context.category_id, context.task_id)
    assert (
        status_code == 200
        and "categories" in modified_todo_json
        and category in modified_todo_json["categories"]
    )


@given(
    "The category with title {category_title} and description {category_description}"
)
def step_impl(context, category_title, category_description):
    """Create a category with the given title and description."""

    # Create the category
    code, category_res = curl(
        "POST",
        CATEGORIES,
        data_style="json",
        response_style="json",
        json={"title": str(category_title), "description": str(category_description)},
    )
    categories = curl("GET", CATEGORIES, response_style="json")[1]["categories"]
    context.category_id = category_res["id"]
    context.category_title = category_res["title"]
    context.category = category_res
    assert code == 201 and category_res in categories


@then("The category should be linked to the task")
def step_impl(context):
    """Check if the category is linked to the task"""

    # Check if the category is linked to the task
    code, content = curl(
        "GET", f"{CATEGORIES}/{int(context.category_id)}", response_style="json"
    )
    modified_category_json = content["categories"][0]

    assert code == 200 and "todos" in modified_category_json


@then("The category should not be linked to the task")
def step_impl(context):
    """Check if the category is not linked to the task"""

    # Check if the category is not linked to the task
    modified_todo = curl(
        "GET",
        f"{TODOS}/{int(context.task_id)}",
        response_style="json",
    )
    modified_todo_json = modified_todo[1]["todos"][0]

    assert modified_todo[0] == 200 and "categories" not in modified_todo_json


@then("The task should not be linked to the category")
def step_impl(context):
    """Check if the task is not linked to the category"""

    categories = curl(
        "GET",
        f"{CATEGORIES}/{int(context.category_id)}",
        response_style="json",
    )
    categories_json = categories[1]["categories"][0]

    assert categories[0] == 200 and "todos" not in categories_json


##########################################################
############## 11_category_title #########################
##########################################################
# Step definition for creating a category with a given title.
@given("Create a category with title {category_title}")
def user_step(context, category_title):
    # Send a POST request to create a new category.
    code, response = curl(
        "POST",
        CATEGORIES,
        data_style="json",
        response_style="json",
        json={"title": category_title},
    )
    # Store the created category's title and ID in the context for later use.
    context.given_title = category_title
    context.cateID = response["id"]
    # Assert that the request was successful.
    assert code == 201


# Step definition for changing the title of a category.
@when("A user changes the title of category to {new_cate_title}")
def user_step(context, new_cate_title):
    # Store the new title in the context.
    context.newCateTitle = new_cate_title
    # Construct the URL for updating the category.
    url = CATEGORIES + "/%d" % int(context.cateID)
    # Send a PUT request to update the category's title.
    status_code, _ = curl(
        "PUT",
        url,
        data_style="json",
        response_style="json",
        json={"title": new_cate_title},
    )
    # Print and assert the response status code.
    print(status_code)
    assert status_code == 200


# Step definition for a failed attempt to change a category's title due to missing JSON input.
@when("A user wants to change the title of category but forgets the json input")
def user_step(context):
    # Attempt to update the category with an empty JSON payload.
    status_code, _ = curl(
        "PUT",
        CATEGORIES + "/%d" % int(context.cateID),
        data_style="json",
        response_style="json",
        json={},
    )
    # Assert that the request fails with a 400 Bad Request error.
    assert status_code == 400


# Step definition for an attempt to change a category's title using a wrong category ID.
@when(
    "A user uses the {wrong_cate_id} to change the title of category to {new_cate_title}"
)
def user_step(context, new_cate_title, wrong_cate_id):
    # Construct the URL with the wrong category ID.
    url = CATEGORIES + "/%d" % int(wrong_cate_id)
    # Send a PUT request to update the category's title with the wrong ID.
    status_code, _ = curl(
        "PUT",
        url,
        data_style="json",
        response_style="json",
        json={"title": new_cate_title},
    )
    # Store and assert the response status code.
    context.NotFound = status_code
    assert status_code == 404


# Step definition to verify that the category's title has been changed.
@then("The category title should be changed")
def user_step(context):
    # Send a GET request to retrieve the updated category.
    status_code, response = curl(
        "GET",
        CATEGORIES + "/%d" % int(context.cateID),
        data_style="json",
        response_style="json",
    )
    # Assert that the title has been updated.
    assert (
        status_code == 200
        and context.newCateTitle == response["categories"][0]["title"]
    )


# Step definition to verify that the category's title remains unchanged after a failed update.
@then("The category title should remain unchanged")
def user_step(context):
    # Send a GET request to check the current category's title.
    status_code, response = curl(
        "GET",
        CATEGORIES + "/%d" % int(context.cateID),
        data_style="json",
        response_style="json",
    )
    # Assert that the title is unchanged.
    assert (
        status_code == 200 and response["categories"][0]["title"] == context.given_title
    )


# Step definition for handling a not found error when a category ID is wrong.
@then("Not found error displays")
def user_step(context):
    # Assert that a 404 Not Found error was received.
    assert context.NotFound == 404


##########################################################
############## 12_change_todo_priority ###################
##########################################################


@given(
    "A user want to update the category under the todo with title {todo_title}, description {todo_description} to a new category with title {todo_category}"
)
def create_todo(context, todo_title, todo_description, todo_category):
    # Create a new todo item with provided title, description, and status
    data = {
        "title": str(todo_title),
        "description": str(todo_description),
        "doneStatus": True,
    }
    status_codePT, newtodo = curl(
        "POST", TODOS, data_style="json", response_style="json", json=data
    )
    context.todo_id = newtodo["id"]  # Store the new todo item's ID in context

    # Add a new category to the created todo item
    url = TODOS + "/%d/categories" % int(context.todo_id)
    cate_title = {"title": str(todo_category)}
    status_codePTC, responseP = curl(
        "POST", url, data_style="json", response_style="json", json=cate_title
    )
    context.todo_cate_id = responseP["id"]  # Store the new category's ID in context
    assert (
        status_codePT == 201 and status_codePTC == 201
    )  # Assert successful creation of todo and category


@when("A user want to delete the old category lable under todos")
def user_step(context):
    # Delete the category associated with the todo item
    codeD, _ = curl(
        "DELETE",
        TODOS + "/%d/categories/%d" % (int(context.todo_id), int(context.todo_cate_id)),
        data_style="json",
        response_style="json",
    )
    assert codeD == 200  # Assert successful deletion


@when("A user want to double delete the old category lable under todos")
def user_step(context):
    # Attempt to delete the already deleted category
    codeD, response = curl(
        "DELETE",
        TODOS + "/%d/categories/%d" % (int(context.todo_id), int(context.todo_cate_id)),
        data_style="json",
        response_style="json",
    )
    assert codeD == 404  # Assert that deletion is not found (already deleted)
    context.NotFound = codeD  # Store the not found status in context


@when("A user want to post a new category with the title {new_todo_category}")
def user_step(context, new_todo_category):
    # Post a new category with a given title to the todo item
    url = TODOS + "/%d/categories" % int(context.todo_id)
    context.new_cate_title = (
        new_todo_category  # Store the new category title in context
    )
    codeP, responseP = curl(
        "POST",
        url,
        data_style="json",
        response_style="json",
        json={"title": new_todo_category},
    )
    assert codeP == 201  # Assert successful posting


@then("The new category under todo would have the new name")
def user_step(context):
    # Retrieve the category information of the todo item
    url = TODOS + "/%d/categories" % int(context.todo_id)
    status_code, response = curl("GET", url, response_style="json")
    # Assert that the response is successful and the category title matches the updated one
    assert (
        status_code == 200
        and response["categories"][0]["title"] == context.new_cate_title
    )


##########################################################
############## 13_change_project_priority ################
##########################################################


@given(
    "A user want to update the category under the project with title {project_title}, description {project_description} to a new category with title {project_category}"
)
def create_project(context, project_title, project_description, project_category):
    # This function is for creating a project with the given title and description, and adding a category to it.
    data = {
        "title": str(project_title),
        "description": str(project_description),
    }
    status_codePT, newproject = curl(
        "POST", PROJECTS, data_style="json", response_style="json", json=data
    )
    context.project_id = newproject["id"]

    # Add category under that project
    url = PROJECTS + "/%d/categories" % int(context.project_id)
    cate_title = {"title": str(project_category)}
    status_codePTC, responseP = curl(
        "POST", url, data_style="json", response_style="json", json=cate_title
    )
    context.project_cate_id = responseP["id"]
    assert status_codePT == 201 and status_codePTC == 201


@when("A user want to delete the old category lable under projects")
def user_step(context):
    # This function is for deleting the previously created category under a project.
    codeD, _ = curl(
        "DELETE",
        PROJECTS
        + "/%d/categories/%d" % (int(context.project_id), int(context.project_cate_id)),
        data_style="json",
        response_style="json",
    )
    assert codeD == 200


@when("A user want to double delete the old category lable under projects")
def user_step(context):
    # This function tries to delete the already deleted category, expecting a 404 error (Not Found).
    codeD, responseD = curl(
        "DELETE",
        PROJECTS
        + "/%d/categories/%d" % (int(context.project_id), int(context.project_cate_id)),
        data_style="json",
        response_style="json",
    )
    assert codeD == 404
    context.NotFound = codeD


@when(
    "A user posts a new category under the project with the title {new_project_category}"
)
def user_step(context, new_project_category):
    # This function is for adding a new category under the project.
    url = PROJECTS + "/%d/categories" % int(context.project_id)
    context.new_cate_title = new_project_category
    codeP, responseP = curl(
        "POST",
        url,
        data_style="json",
        response_style="json",
        json={"title": new_project_category},
    )
    context.project_new_cate_id = responseP["id"]
    assert codeP == 201


@then("The new category under project would have the new name")
def user_step(context):
    # This function checks if the new category under the project has the updated name.
    url = PROJECTS + "/%d/categories" % int(context.project_id)
    status_code, response = curl("GET", url, response_style="json")
    print(response)
    # Not empty and response title = the one updated
    assert (
        status_code == 200
        and response["categories"][0]["title"] == context.new_cate_title
    )


@then("The new category created secondly under project would have the new name")
def user_step(context):
    # This function checks if the second new category created under the project has the updated name.
    url = PROJECTS + "/%d/categories" % int(context.project_id)
    status_code, response = curl("GET", url, response_style="json")
    print(response)
    # Not empty and response title = the one updated
    assert (
        status_code == 200
        and response["categories"][0]["title"] == context.new_cate_title
    )
    print(context.project_cate_id)
    # BUG: The deleted project still occupies an id, so that the new-post project can not inherit the previous id
    assert context.project_new_cate_id == context.project_cate_id


##########################################################
############## 14_drop_add_newproject ####################
##########################################################


# Defines a step for creating a project with a given title and description
@given(
    "A user created a project with title {project_title}, description {project_description}"
)
def create_project(context, project_title, project_description):
    # Assemble project data
    data = {
        "title": str(project_title),
        "description": str(project_description),
    }
    status_codeP, response = curl("POST", PROJECTS, response_style="json", json=data)
    context.project_id = response["id"]
    assert status_codeP == 201


# Defines a step for deleting an old project
@when("A user deletes the old project")
def user_step(context):
    codeD, responseD = curl(
        "DELETE",
        PROJECTS + "/%d" % (int(context.project_id)),
        data_style="json",
        response_style="json",
    )
    assert codeD == 200


# Defines a step for creating a new project with specific title and description
@when(
    "A user create a new project with title {new_project_title} and description {new_project_description}"
)
def user_step(context, new_project_title, new_project_description):
    # Assemble new project data
    newData = {
        "title": str(new_project_title),
        "description": str(new_project_description),
    }
    context.new_project_title = new_project_title
    codeP, responseP = curl("POST", PROJECTS, data_style="json", json=newData)
    assert codeP == 201


# Defines a step to verify if the new project is listed among projects
@then("The renewed project should be shown in the list of projects")
def user_step(context):
    # Send GET request to retrieve list of projects
    status_code, response = curl("GET", PROJECTS, response_style="json")
    title_exists = any(
        project.get("title") == str(context.new_project_title)
        for project in response.get("projects", [])
    )
    assert status_code == 200 and title_exists == True


# ----- Alternative flow steps -----


# Defines a step for updating an old project with a new title and description
@when(
    "A user update the old project with new title {new_project_title} and description {new_project_description}"
)
def user_step(context, new_project_title, new_project_description):
    context.new_project_title = new_project_title
    # Assemble updated project data
    newData = {
        "title": str(new_project_title),
        "description": str(new_project_description),
    }
    url = PROJECTS + "/%d" % (int(context.project_id))
    codeP, responseP = curl("PUT", url, data_style="json", json=newData)
    assert codeP == 200


# Defines a step for a failed attempt to update a project with a wrong ID
@when(
    "A not smart user update the old project with new title {new_project_title} and description {new_project_description} but with wrong id {wrong_id}"
)
def user_step(context, new_project_title, new_project_description, wrong_id):
    # Store new project title in context for later use
    context.new_project_title = new_project_title
    newData = {
        "title": str(new_project_title),
        "description": str(new_project_description),
    }
    # Define URL for PUT request with a wrong ID
    url = PROJECTS + "/%d" % (int(wrong_id))
    codePut, responseP = curl("PUT", url, data_style="json", json=newData)
    context.NotFound = codePut
    assert codePut == 404


##########################################################
############## 15_fix_category ###########################
##########################################################


@given(
    "A user wants to create a category with title {category_title} and contains a todo with title {pTodo_title} but wrongly created project instead of todo"
)
def create_project(context, category_title, pTodo_title):
    # Create a category and mistakenly create a project instead of a todo
    code, response = curl(
        "POST",
        CATEGORIES,
        data_style="json",
        response_style="json",
        json={
            "title": str(category_title),
        },
    )
    context.cateID = response["id"]
    url = CATEGORIES + "/%d/projects" % int(context.cateID)
    context.todoTitle = pTodo_title
    pTodo_title = {"title": str(pTodo_title)}
    code2, reponse2 = curl("POST", url, response_style="json", json=pTodo_title)
    context.projectID = reponse2["id"]
    assert code == 201 and code2 == 201


@when("A user deletes the wrong_project under category")
def user_step(context):
    # Delete the previously created wrong project under a category
    urlD = CATEGORIES + "/%d/projects/%d" % (
        int(context.cateID),
        int(context.projectID),
    )
    codeD, responseD = curl("DELETE", urlD, data_style="json", response_style="json")
    assert codeD == 200


@when("A user wrongly deletes twice the wrong_project under category")
def user_step(context):
    # Attempt to delete the same wrong project twice under a category
    urlD = CATEGORIES + "/%d/projects/%d" % (
        int(context.cateID),
        int(context.projectID),
    )
    codeD, responseD = curl("DELETE", urlD, data_style="json", response_style="json")
    assert codeD == 404
    context.NotFound = codeD


@when("A user create the correct_todo under category with title {pTodo_title}")
def user_step(context, pTodo_title):
    # Create the correct todo under a category
    urlP = CATEGORIES + "/%d/todos" % int(context.cateID)
    codeP, responseP = curl(
        "POST", urlP, data_style="json", json={"title": pTodo_title}
    )
    assert codeP == 201


@when(
    "A not smart user create the correct_todo under category with title {pTodo_title} but with wrong id {wrongID}"
)
def user_step(context, pTodo_title, wrongID):
    # Attempt to create a correct todo under a category with a wrong ID
    urlP = CATEGORIES + "/%d/todos" % int(wrongID)
    codeP, responseP = curl(
        "POST", urlP, data_style="json", json={"title": pTodo_title}
    )
    context.NotFound = codeP
    assert codeP == 404


@then("The todo under category should be created successfully and has the right name")
def user_step(context):
    # Verify that the todo under the category is created successfully with the correct name
    url = CATEGORIES + "/%d/todos" % int(context.cateID)
    status_code, response = curl("GET", url, response_style="json")
    # Not empty and response title = the one updated
    print(response["todos"][0]["title"])
    print(context.todoTitle)
    assert status_code == 200 and response["todos"][0]["title"] == context.todoTitle
