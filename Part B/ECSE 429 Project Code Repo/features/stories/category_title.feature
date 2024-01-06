Feature: Category Management
    As a user,
    I want to change the title of a category, 
    to specify the works.

    # Normal Flow
    Scenario Outline: Update the title of an existing category
        Given Create a category with title <category_title>
        When A user changes the title of category to <new_cate_title>
        Then The category title should be changed
        Examples:
            | category_title | new_cate_title  |
            | High           | Middle          |
            | Middle         | Low             |
            | Low            | High            |  

    # Alternative Flow
    Scenario Outline: Attempt to update the title of an existing category without specify the new title
        Given Create a category with title <category_title>
        When A user wants to change the title of category but forgets the json input
        Then The category title should remain unchanged
        Examples:
            | category_title |
            | High           |
            | Middle         |
            | Low            |

    # Error Flow
    Scenario Outline: Attempt to update the title of a category but get wrong on the id of the category
        Given Create a category with title <category_title> 
        When A user uses the <wrong_cate_id> to change the title of category to <new_cate_title>
        Then Not found error displays
        Examples:
            | category_title | wrong_cate_id | new_cate_title  |
            | High           | 9999          | Middle          |
            | Middle         | -1            | Low             |
            | Low            | 1001          | High            | 
