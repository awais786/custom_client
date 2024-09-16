# API Clients: InstructorClient & CourseClient

This module contains specialized clients for interacting with instructor and course-related operations on an API. Both `InstructorClient` and `CourseClient` inherit from a base class `BaseClient` and utilize dynamic endpoint generation from configuration files.

## Features

- **InstructorClient**: Handles instructor-specific operations like listing tasks and managing exams.
- **CourseClient**: Handles course-specific operations like retrieving course details, managing course content, etc.
- Both clients dynamically load API endpoints from JSON configuration files. ( Right now using hardcoded json from client )
- Simplifies interaction with various API endpoints related to instructors and courses.

## Installation

To use `InstructorClient` and `CourseClient`, ensure that both classes are included in your project along with their dependency, `BaseClient`.

```python
from openedxclient import OpenEdxClient
# generate token with superuser perms due to instructor requirments or give proper role in courseroles tables.

```Get CSRF TOKEN
 curl --location --request GET 'http://localhost:18000/csrf/api/v1/token'
```GET access Token Use this [link](https://discuss.openedx.org/t/authenticate-with-oauth-token-to-access-api-endpoints-instructor-apis/13658) for more details.

curl --location 'http://localhost:18000/oauth2/access_token' \
--form 'client_id="client_id"' \
--form 'client_secret="client_secret"' \
--form 'token_type="jwt"' \
--form 'grant_type="client_credentials"'


headers = {'Authorization': 'JWT ' + accesstoken, 'X-CSRFToken' : csrftoken}  # generate token with superuser perms due to instructor requirments.
api_client = OpenEdxClient(base_url='http://localhost:18000', headers=headers)

# The InstructorClient provides an easy way to perform course-related operations on a specific course.
ins_client = api_client.instructor(course_id='course-v1:edx+cs222+2015_t5')
ins_client.role_members(data={'rolename': 'instructor'})
ins_client.student_progress_url(data={'unique_student_identifier': 'staff@example.com'})
ins_client.anonymous_ids()

# The CourseClient provides an easy way to perform course-related operations on a specific course.
course_client = api_client.course(course_id='course-v1:edx+cs222+2015_t5')
course_client.get_course_details()



