Feature: Update Todo's Category 
  As a user,
  I want to update the todos’ priorty, 
  to better manage the tasks wait to be done.

  # Normal Flow
  Scenario Outline: Update the category of a todo
    Given A user want to update the category under the todo with title <todo_title>, description <todo_description> to a new category with title <todo_category>
    When A user want to delete the old category lable under todos
    And A user want to post a new category with the title <new_todo_category>
    Then The new category under todo would have the new name

    Examples:
      | todo_title   | todo_description | todo_category | new_todo_category |
      | Homework     | Math exercises   | MEDIUM        | HIGH              |
      | Study Group  | Prepare slides   | HIGH          | MEDIUM            |
      | Gym Session  | Evening workout  | LOW           | MEDIUM            |

  # Alternative Flow
  Scenario Outline: Update the category of a todo by posting new first then deleting old
    Given A user want to update the category under the todo with title <todo_title>, description <todo_description> to a new category with title <todo_category>
    When A user want to post a new category with the title <new_todo_category>
    And A user want to delete the old category lable under todos
    Then The new category under todo would have the new name

    Examples:
      | todo_title  | todo_description | todo_category | new_todo_category |
      | Assignment  | Write report     | LOW           | HIGH              |
      | Presentation| Company overview | MEDIUM        | HIGH              |
      | Laundry     | Wash clothes     | LOW           | LOW               |

  # Error Flow
  Scenario Outline: Attempt to update a category under todo but deleted the old catagory twice
    Given A user want to update the category under the todo with title <todo_title>, description <todo_description> to a new category with title <todo_category>
    When A user want to delete the old category lable under todos
    And A user want to double delete the old category lable under todos
    Then Not found error displays

    Examples:
      | todo_title  | todo_description | todo_category | new_todo_category |
      | Video Game  | Evening relax    | LOW           | MEDIUM            |
      | Book Reading| Finish chapter   | MEDIUM        | HIGH              |
      | Shopping    | Grocery purchase | LOW           | MEDIUM            |
