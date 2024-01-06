# Software Validation Project

## Contents
1. [Part A: Exploratory Testing of REST API](#part-a-exploratory-testing-of-rest-api)
2. [Part B: Story Testing of REST API](#part-b-story-testing-of-rest-api)
3. [Part C: Non-Functional Testing of REST API](#part-c-non-functional-testing-of-rest-api)

## Part A: Exploratory Testing of REST API
### 1. Exploratory Testing of REST API Application
- **Objective:** To conduct exploratory testing on a REST API-based Todo List Manager.
- **Approach:** Employ Charter Driven Session-Based Exploratory Testing to understand the application's behavior. Team members may work individually or in pairs.
- **Tasks:**
  - Identify both documented and undocumented features of the application.
  - Develop scripts or programs to showcase these capabilities.
  - Test the application with typical data scenarios.

### 2. Unit Test Suite
- **Objective:** Develop a comprehensive unit test suite for the REST API Todo List Manager using JUnit or a similar framework.
- **Requirements:**
  - Create tests for each API endpoint identified during exploratory testing.
  - Verify API functionality and uncover potential bugs.
  - Tests should support JSON and XML payloads and command-line interactions.
  - Ensure system stability throughout the testing process.

### 3. Bug Summary and Reporting
- **Objective:** Establish a systematic process for bug tracking and reporting.
- **Requirements:** 
  - Develop a bug report template covering key details such as executive summary, bug description, impact assessment, and reproduction steps.
  - Select a suitable bug tracking tool.

## Part B: Story Testing of REST API
### User Stories
- **Objective:** Craft five user stories per team member, based on the API explored in Part A.
- **Format:** Stories should adhere to the structure: "As a [user], I want [action] so that [benefit]."
- **Domain:** Teams are free to choose any relevant domain.

### Story Test Suite
- **Acceptance Tests:** 
  - Develop a minimum of three acceptance tests for each story, covering normal, alternate, and error flows.
- **Gherkin Scripts:** 
  - Define story tests using Gherkin syntax in feature files, including a 'Background' section for initial conditions.
- **Requirements:** 
  - Design tests for execution with varying data sets.

### Story Test Automation
- **Tools:** Utilize Cucumber or a similar tool for Gherkin script interpretation and execution.
- **Step Definitions:**
  - Develop step definitions for controlling the REST API Todo List Manager from Part A.
  - Design these definitions as reusable components.
- **Code Quality:** Adhere to Clean Code principles by Robert C. Martin.
- **Gherkin Script Features:**
  - Ensure accuracy and consistency.
  - Reset the system to its initial state after test completion.
  - Allow for independent execution of tests.

### Additional Considerations
- **Story Tests:** Confirm that tests fail when the service is unavailable.
- **Bug Reporting:** Follow the same reporting format as in Part A, linking bugs to their respective stories.

## Part C: Non-Functional Testing of REST API
### Performance Testing
- **Objective:** Execute performance testing through dynamic analysis.
- **Tasks:**
  - Develop a program using the API from Part A that populates objects with random data.
  - Modify unit test code from Part A to time create, delete, and update operations.
  - Conduct experiments to evaluate performance scalability with increasing data volumes.
  - Utilize tools like Windows PerfMon, Mac Activity Monitor, or Linux vmstat for monitoring CPU and memory usage during tests.

### Static Analysis
- **Tool:** Employ SonarQube Community Edition for static code analysis.
- **Objective:** Analyze the source code of the REST API Todo List Manager.
- **Tasks:**
  - Provide recommendations for code modifications to mitigate risks in future updates, enhancements, or bug fixes.
  - Examine aspects such as code complexity, statement counts, and potential technical risks or code smells identified by the analysis.
