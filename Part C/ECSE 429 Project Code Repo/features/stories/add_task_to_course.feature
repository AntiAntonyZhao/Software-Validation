Feature: Add a task to a course to do list

    As a student, I add a task to a course to do list, so I can remember it.

    # Normal flow
    Scenario Outline: Add a new task to course to do list
        Given An existing project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
        When A user adds a task with title <task_title>, description <task_description> and done status <task_done_status> to the project
        Then This task should be contained in the course to do list 
        And The project should be associated to the task
        Examples:
            | project_title | project_completed | project_active | project_description | task_title  | task_description | task_done_status | 
            | ECSE 429      | False             | True           | Sofaaaon course     | Hello world | asdf             | False           | 
            | COMP 360      | False             | True           | Todss60             | A3          | data3            | False           |

    # Alternate flow
    Scenario Outline: Add a completed task to course to do list 
        Given An existing project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
        When A user adds a task with title <task_title>, description <task_description> and done status <task_done_status> to the project
        Then This task should be contained in the course to do list 
        And The project should be associated to the task
        Examples:
            | project_title | project_completed | project_active | project_description | task_title  | task_description | task_done_status | 
            | ECSE 429      | False             | True           | Sofaaaon course     | Hello world | asdf             | True            | 
            | COMP 360      | False             | True           | Todss60             | A3          | data3            | True            |

    # Error flow
    Scenario Outline: Add a task to a project that does not exist
        Given An existing project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
        When A user adds a task that does not exist with title <task_title>, description <task_description> and done status <task_done_status> to the project 
        Then we should receive an error message
        Examples:
            | project_title | project_completed | project_active | project_description | task_title  | task_description | task_done_status | 
            | ECSE 429      | False             | True           | Sofaaaon course     | Hello world | asdf             | True            | 
            | COMP 360      | False             | True           | Todss60             | A3          | data3            | True            |