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


# Add oauth application with following data
# http://localhost:18000/admin/oauth2_provider/application/

# Add new client with following credentials.
# "client_id": "client_id",
# "client-secret: "client_secret"
# "user": "service username"
# "grant_type": "client_credentials",
# "client-type": "confidential"

# service username must be is-superuser=True or create a role in course access roles.

from openedxclient import OpenEdxClient
base_url='http://localhost:18000/'
course_id='course-v1:edx+cs222+2015_t5'
client_id = 'client_id'
client_secret= "client_secret"
unique_student_identifier = 'staff@example.com'
api_client = OpenEdxClient(base_url=base_url).authenticate(client_id=client_id, client_secret=client_secret)
print('************** Instructor **************')
print("Accessing instructor endpoints")
ins_client = api_client.instructor(course_id=course_id)
print("Role members:")
resp = ins_client.role_members(rolename='instructor')
print(resp._content)
print(" student_progress_url:")
resp = ins_client.student_progress_url(unique_student_identifier=unique_student_identifier)
print(resp._content)
print("anonymous_ids:")
resp = ins_client.anonymous_ids()
print(resp._content)
print("entrance_exam_tasks:")
resp = ins_client.entrance_exam_tasks(unique_student_identifier=unique_student_identifier)
print(resp._content)
print("register_and_enroll:")
resp = ins_client.register_and_enroll()
print(resp._content)
print("email_content:")
resp = ins_client.email_content()
print(resp._content)
print('************** Courses **************')
print("Accessing course endpoints")
course_client = api_client.course(course_id=course_id)
resp = course_client.get_course_details()
print("course details:")
print(resp._content)

