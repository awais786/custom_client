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
The InstructorClient provides an easy way to perform instructor-related operations on a specific course.

data =  {'unique_student_identifier':  'teststudent@gmail.com'} 
headers = {"content-type": "application/json"}
headers = {'HTTP_AUTHORIZATION': 'JWT ' + self.jwt_token}  # generate token with superuser perms due to instructor requirments.

instructor_client = InstructorClient(course_id='course-v1:edX+DemoX+T2024')
tasks = instructor_client.list_tasks()
url = instructor_client.get_student_progress_url(data=data, headers=headers)

The CourseClient provides an easy way to perform course-related operations on a specific course.

course_client = CourseClient(course_id='course-v1:edX+DemoX+T2024')
course_client.get_course_details(headers=headers)
