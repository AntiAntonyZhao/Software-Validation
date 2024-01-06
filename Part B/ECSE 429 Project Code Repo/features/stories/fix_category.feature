Feature: Manage sub-nodes of Categories
    As a user,
    I want fix the mistake of wanting a todo but wrongly created a project under categories,
    so that I can get a correct todo under categories.

    # Normal Flow
    Scenario Outline: Fix the problem by first deleting the wrong project and then creating a todo under categories
        Given A user wants to create a category with title <category_title> and contains a todo with title <pTodo_title> but wrongly created project instead of todo
        When A user deletes the wrong_project under category
        And A user create the correct_todo under category with title <pTodo_title>
        Then The todo under category should be created successfully and has the right name
        Examples:
            | category_title | pTodo_title        |
            | High           | Final Exam         |
            | Middle         | Group Project      |
            | Low            | Daily Assignment   |

    # Alternative Flow
    Scenario Outline: Fix the problem by first creating a todo and then deleting the wrong project under categories
        Given A user wants to create a category with title <category_title> and contains a todo with title <pTodo_title> but wrongly created project instead of todo
        When A user create the correct_todo under category with title <pTodo_title>
        And A user deletes the wrong_project under category
        Then The todo under category should be created successfully and has the right name
        Examples:
            | category_title | pTodo_title        |
            | High           | Final Exam         |
            | Middle         | Group Project      |
            | Low            | Daily Assignment   |

    # Error Flow 1
    Scenario Outline: Attempt to fix the problem but wrongly deleting the wrong project twice under categories
        Given A user wants to create a category with title <category_title> and contains a todo with title <pTodo_title> but wrongly created project instead of todo
        When A user deletes the wrong_project under category
        And A user wrongly deletes twice the wrong_project under category
        Then Not found error displays
        Examples:
            | category_title | pTodo_title        |
            | High           | Final Exam         |
            | Middle         | Group Project      |
            | Low            | Daily Assignment   |


    # Error Flow 2
    Scenario Outline: Attempt to fix the problem but wrongly created a todo under categories with wrong category ID
        Given A user wants to create a category with title <category_title> and contains a todo with title <pTodo_title> but wrongly created project instead of todo
        When A user deletes the wrong_project under category
        And A not smart user create the correct_todo under category with title <pTodo_title> but with wrong id <wrongID>
        Then Not found error displays
        Examples:
            | category_title | pTodo_title        | wrongID |
            | High           | Final Exam         | 100     |
            | Middle         | Group Project      | -1      |
            | Low            | Daily Assignment   | 999     |



