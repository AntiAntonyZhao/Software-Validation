# As a student, I mark a task as done on my course to do list, so I can track my accomplishments.

Feature: Change task done status
    As a student, 
    I mark a task as done on my course to do list, 
    so I can track my accomplishments.

    # Normal Flow
    Scenario Outline: Mark a task as done
        Given A task with title <task_title>, description <task_description> and done status <task_done_status>
        When A user marks the task <task_title> as done
        Then The task should have a a doneStatus of <final_task_done_status>
        Examples:
            | task_title  | task_description | task_done_status | final_task_done_status | 
            | write essay | essay #4         | False           | True                  |
            | read paper  | paper #3         | True            | True                  |
            | project 1   | class #4         | False           | True                  |


    # Alternative Flow
    Scenario Outline: Mark a task as not done
        Given A task with title <task_title>, description <task_description> and done status <task_done_status>
        When A user marks the task <task_title> as not done
        Then The task should have a a doneStatus of <final_task_done_status>
        Examples:
            | task_title  | task_description | task_done_status | final_task_done_status | 
            | write essay | essay #4         | True            | False                 |
            | read paper  | paper #3         | True            | False                 |
            | project 1   | class #4         | False           | False                 |


    # Error Flow
    Scenario Outline: Mark a non-exitent task as done
        Given A task with title <task_title>, description <task_description> and done status <task_done_status>
        When A user marks the wrong task <wrong_task_id> as done
        Then There should be a 404 NotFound error
        Examples:
            | task_title  | task_description | task_done_status | final_task_done_status | wrong_task_id    |
            | write essay | essay #4         | False           | True                  | -1               |
            | read paper  | paper #3         | True            | True                  | 0                |
            | project 1   | class #4         | False           | True                  | -999             |
