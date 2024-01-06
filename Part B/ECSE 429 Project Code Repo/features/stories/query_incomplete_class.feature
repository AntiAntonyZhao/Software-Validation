# As a student,I query the incomplete tasks for a class I am taking,to help manage my time.

Feature: Query incomplete tasks for class 

    As a student,
    I query the incomplete tasks for a class I am taking,
    to help manage my time.

    # Normal Flow
    Scenario Outline: 1 incomplete task for class
        Given A task with description <task_description>, task <task_title>, and done status <task_done_status> linked to project with title <project_title>, done status <project_completed>, active status <project_active> and description <project_description>
        # And A complete task with title <task_title>, description <task_description> linked to project
        Then Only incomplete task for class should be returned
        Examples:
            | task_title  | task_description | task_done_status | project_title | project_completed | project_active | project_description    |
            | write essay | essay #4         | False           | COMP 360      | False             | True           | Todo list for COMP 360 |
            | read paper  | paper #3         | False           | ECSE 429      | False             | True           | ecse 429 stuff         |
            | project 1   | class #4         | False           | ECSE 422      | False             | True           | some things            |
    
    # Alternative Flow
    Scenario Outline: 0 incomplete tasks for class
        Given A task with description <task_description>, task <task_title>, and done status <task_done_status> linked to project with title <project_title>, done status <project_completed>, active status <project_active> and description <project_description>
        # And A complete task with title <task_title>, description <task_description> linked to project
        Then No tasks for class should be returned
        Examples:
            | task_title  | task_description | task_done_status | project_title | project_completed | project_active | project_description    |
            | write essay | essay #4         | True           | COMP 360      | False             | True           | Todo list for COMP 360 |
            | read paper  | paper #3         | True           | ECSE 429      | False             | True           | ecse 429 stuff         |
            | project 1   | class #4         | True           | ECSE 422      | False             | True           | some things            |

    # Error Flow
    Scenario Outline: No doneStatus filter used for class
        Given A task with description <task_description>, task <task_title>, and done status <task_done_status> linked to project with title <project_title>, done status <project_completed>, active status <project_active> and description <project_description>
        Then Tasks for class should be returned
        Examples:
            | task_title  | task_description | task_done_status | category_title| category_description | task_notDoneStatus |
            | write essay | essay #4         | False           | HIGH          | high priority         | TRUE               |
            | read paper  | paper #3         | False           | HIGH          | high priority         | TRUE               |
            | project 1   | class #4         | False           | HIGH          | high priority         | TRUE               |