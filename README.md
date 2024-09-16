# API Clients: InstructorClient & CourseClient

This module contains specialized clients for interacting with instructor and course-related operations on an API. Both `InstructorClient` and `CourseClient` inherit from a base class `BaseClient` and utilize dynamic endpoint generation from configuration files.

## Features

- **InstructorClient**: Handles instructor-specific operations like listing tasks and managing exams.
- **CourseClient**: Handles course-specific operations like retrieving course details, managing course content, etc.
- Both clients dynamically load API endpoints from JSON configuration files.
- Simplifies interaction with various API endpoints related to instructors and courses.

## Installation

To use `InstructorClient` and `CourseClient`, ensure that both classes are included in your project along with their dependency, `BaseClient`.

```python
from instructor_client import InstructorClient
from course_client import CourseClient

## Usage
InstructorClient
The InstructorClient provides an easy way to perform instructor-related operations on a specific course.

Constructor
data =  {'unique_student_identifier':  user.email}  # user should be superuser due to instructor requirments.
headers = {"content-type": "application/json"}
headers = {'HTTP_AUTHORIZATION': 'JWT ' + self.jwt_token}

instructor_client = InstructorClient(course_id='course-v1:edX+DemoX+T2024')
# List tasks for a course
tasks = instructor_client.list_tasks()
url = instructor_client.get_student_progress_url(data=data, headers=headers)


course_client = CourseClient(course_id='course-v1:edX+DemoX+T2024')
course_client.get_course_details(headers=headers)
