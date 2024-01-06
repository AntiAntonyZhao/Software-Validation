Feature: Projects Management
    As a user,
    I want to replace a project object with newer version by delete-recreate,
    to better managing my projects list.

    # Normal Flow
    Scenario Outline: Update a project by deleting the old one and creating a new project
        Given A user created a project with title <project_title>, description <project_description>
        When A user deletes the old project 
        And A user create a new project with title <new_project_title> and description <new_project_description>
        Then The renewed project should be shown in the list of projects
        Examples:
            | project_title  | project_description | new_project_title | new_project_description |
            | Aa             | ProjectA            | Project A         | First Project           |
            | Bb             | ProjectB            | Project B         | Second Project          |
            | Cc             | ProjectC            | Project C         | Third Project           |

    # Alternative Flow
    Scenario Outline: Replace the old project with a new project without deletion
        Given A user created a project with title <project_title>, description <project_description>
        When A user update the old project with new title <new_project_title> and description <new_project_description>
        Then The renewed project should be shown in the list of projects
        Examples:
            | project_title  | project_description | new_project_title | new_project_description |
            | Aa             | ProjectA            | Project A         | First Project           |
            | Bb             | ProjectB            | Project B         | Second Project          |
            | Cc             | ProjectC            | Project C         | Third Project           |

    # Error Flow
    Scenario Outline: Attempt to replace the old project with a new project but get wrong on the id of the category
        Given A user created a project with title <project_title>, description <project_description>
        When A not smart user update the old project with new title <new_project_title> and description <new_project_description> but with wrong id <wrong_id>
        Then Not found error displays
        Examples:
            | project_title  | project_description | new_project_title | new_project_description | wrong_id |
            | Aa             | ProjectA            | Project A         | First Project           | 100      |
            | Bb             | ProjectB            | Project B         | Second Project          | -50      |
            | Cc             | ProjectC            | Project C         | Third Project           | 999      |
