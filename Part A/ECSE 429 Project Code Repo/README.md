
# ECSE 429 Final Porject
## Part A - Unit Test

Setup Environment:
- Windows 10/11
- python >= 3.8
- `pip install -r requirements.txt`
  
Tree:  `tree -I *__pycache__*`
Run Test: `./test.bat`
Run Test with failing test: `./test_server_down.bat`

    ├── ProjectExecution
    ├── README.md
    ├── SessionNotes
    │   ├── SessionNotes_categories.txt
    │   ├── SessionNotes_projects.txt
    │   ├── SessionNotes_todos.txt
    │   ├── project_5_30.png
    │   ├── project_5_33.png
    │   ├── project_5_50.png
    │   └── project_5_53.png
    ├── starter.bat
    ├── Todo-Manager-swagger.json
    ├── abnormal.ini
    ├── requirements.txt
    ├── rest-api-challenges-single-player.data.txt
    ├── runTodoManagerRestAPI-1.5.5.jar
    ├── test.bat
    ├── test_server_down.bat
    └── tests
        ├── __init__.py
        ├── categories
        │   ├── __init__.py
        │   ├── category_test_data.py
        │   └── test_categories.py
        ├── config.py
        ├── conftest.py
        ├── projects
        │   ├── __init__.py
        │   ├── project_test_data.py
        │   └── test_projects.py
        ├── supplement
        │   ├── __init__.py
        │   ├── additional_test_data.py
        │   ├── test_additional_test.py
        │   └── test_unexpected.py
        ├── todos
        │   ├── __init__.py
        │   ├── test_todos.py
        │   └── todos_test_data.py
        └── utils.py