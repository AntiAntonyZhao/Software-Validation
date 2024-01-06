Feature: Create a to do list for a new class.

  As a student, I create a to do list for a class I am taking, so I can manage course work.

  # Normal flow
  Scenario Outline: Create a to do list for a non-completed class class
    Given there is not a project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
    When A user creates a project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
    Then The projects should contain a project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
    Examples:
      | project_title | project_completed | project_active | project_description    |
      | COMP 360      | False             | True           | Todo list for COMP 360 |
      | ECSE 429      | False             | True           | ecse 429 stuff         |


  # Alternate Flow
  Scenario Outline: Create an inactive and completed to do list for a new class
    Given there is not a project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
    When A user creates a project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
    Then The projects should contain a project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
    Examples:
      | project_title | project_completed | project_active | project_description |
      | ECSE 429      | True             | False           | Sofaaaon course     |
      | COMP 360      | True             | False           | Todss60             |


  Scenario Outline: Create a to do list for a new class with an id
    Given there is not a project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
    When A user creates a project with id <id>
    Then The projects should not contain a project with title <project_title>, description <project_description>, complete status <project_completed> and active status <project_active>
    Examples:
      | project_title | project_completed | project_active | project_description | id |
      | ECSE 429      | False             | True           | Sofaaaon course     | 1  |
      | COMP 360      | False             | True           | Todss60             | 1  |
