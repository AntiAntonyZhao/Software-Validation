# As a student, I want to change a task description, to better represent the work to do.
Feature: Change task description
    As a student, 
    I want to change a task description, 
    to better represent the work to do.

    # Normal Flow
    Scenario Outline: Change task description
        Given A task with title <task_title>, description <task_description> and done status <task_done_status>
        When A user changes the description to <new_task_description>
        Then The task description should be changed
        Examples:
            | task_title  | task_description | task_done_status | new_task_description |
            | write essay | essay #4         | False           | new essay #4         |
            | read paper  | paper #3         | True            | old paper #3         |
            | project 1   | class #4         | False           | cool class #4        |

    # Alternative Flow
    Scenario Outline: Remove task description
        Given A task with title <task_title>, description <task_description> and done status <task_done_status>
        When A user removes the task description
        Then The task description should be empty
        Examples:
            | task_title  | task_description | task_done_status |
            | write essay | essay #4         | False           |
            | read paper  | paper #3         | True            |
            | project 1   | class #4         | False           |

    # Error Flow
    Scenario Outline: Change description of a non-existent task
        Given A task with title <task_title>, description <task_description> and done status <task_done_status>
        When A user selects the <wrong_task_id> to change the description to <new_task_description>
        Then There should be a 404 NotFound error
        Examples:
            | task_title  | task_description | task_done_status | new_task_description | wrong_task_id |
            | write essay | essay #4         | False           | wrong                | -1            |
            | read paper  | paper #3         | True            | ok                   | 0             |
            | project 1   | class #4         | False           | test                 | -99           |

