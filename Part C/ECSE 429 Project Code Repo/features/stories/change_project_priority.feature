Feature: Update Project's Category
  As a user,
  I want to update the projects’ priorty, 
  to better manage the tasks wait to be done.

  # Normal Flow
  Scenario Outline: Update the category of a project
    Given A user want to update the category under the project with title <project_title>, description <project_description> to a new category with title <project_category>
    When A user want to delete the old category lable under projects
    And A user posts a new category under the project with the title <new_project_category>
    Then The new category created secondly under project would have the new name

    Examples:
      | project_title   | project_description | project_category | new_project_category |
      | Homework        | Math exercises      | MEDIUM           | HIGH              |
      | Study Group     | Prepare slides      | HIGH             | MEDIUM            |
      | Gym Session     | Evening workout     | LOW              | MEDIUM            |

  # Alternative Flow
  Scenario Outline: Update the category of a project by posting new first then deleting old
    Given A user want to update the category under the project with title <project_title>, description <project_description> to a new category with title <project_category>
    When A user posts a new category under the project with the title <new_project_category>
    And A user want to delete the old category lable under projects
    Then The new category under project would have the new name

    Examples:
      | project_title  | project_description | project_category | new_project_category |
      | Assignment  | Write report     | LOW           | HIGH              |
      | Presentation| Company overview | MEDIUM        | HIGH              |
      | Laundry     | Wash clothes     | LOW           | LOW               |

  # Error Flow
  Scenario Outline: Attempt to update a category under todo but deleted the old catagory twice
    Given A user want to update the category under the project with title <project_title>, description <project_description> to a new category with title <project_category>
    When A user want to delete the old category lable under projects
    And A user want to double delete the old category lable under projects
    Then Not found error displays

    Examples:
      | project_title  | project_description | project_category | new_project_category |
      | Video Game  | Evening relax    | LOW           | MEDIUM            |
      | Book Reading| Finish chapter   | MEDIUM        | HIGH              |
      | Shopping    | Grocery purchase | LOW           | MEDIUM            |
