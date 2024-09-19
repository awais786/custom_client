# API Clients: InstructorClient & CourseClient

This module provides specialized clients (`InstructorClient` and `CourseClient`) to interact with instructor and course-related operations on an API. Both clients inherit from a base class `BaseClient` and use dynamic endpoint generation based on configuration.

## Features

- **InstructorClient**: Supports instructor-specific operations such as listing tasks and managing exams.
- **CourseClient**: Handles course-related operations, including retrieving course details and managing content.
- Both clients dynamically load API endpoints from configuration files (currently hardcoded in the client).
- Simplifies interactions with various instructor and course-related API endpoints.

## Installation

To use `InstructorClient` and `CourseClient`, include both classes along with their dependency, `BaseClient`, in your project.

## Setup

To interact with the API, you need to authenticate with a token that has superuser permissions (for instructor actions) or assign proper roles in the `CourseRoles` table.

### OAuth Client Setup

1. Visit the admin panel of your OAuth provider:  
   `http://localhost:18000/admin/oauth2_provider/application/`
   
2. Add a new OAuth application with the following credentials:
   - `client_id`: **client_id**
   - `client_secret`: **client_secret**
   - `user`: **service username**
   - `grant_type`: `client_credentials`
   - `client_type`: `confidential`

### Local Testing

For testing purposes, a sample Django app has been added in the `mockserver` folder. This lets you test the clients locally without requiring any external service or the OAuth setup above.

#### Instructions for Local Testing

1. Set up two environments:
   - One for running the Django server.
   - Another for executing the test script.

2. Run the following commands:

   **First terminal**:  
   Start the Django server:
   ```bash
   make requirements
   make runserver
   
3. Run the following client:
    **Second terminal**:
   ```bash
   make actual-client-testing

4. Run the tests with live django app:
    **Second terminal**:
   ```bash
   make run-tests


## Script Overview

The script performs the following actions:

- **Authenticate** using the `OpenEdxClient` with provided credentials.
- **Instructor Endpoints**: Fetch members of a specific role (e.g., `instructor`).
- **Course Endpoints**: Fetch course details using the course ID.

### Script Usage

#### Authentication and Client Initialization

```python
from openedxclient import OpenEdxClient

# Define API credentials and course information
base_url = 'http://localhost:8000/'
course_id = 'course-v1:edx+cs222+2015_t5'
client_id = 'client_id'
client_secret = 'client_secret'
unique_student_identifier = 'staff@example.com'

# Authenticate and initialize the OpenEdxClient
api_client = OpenEdxClient(base_url=base_url).authenticate(client_id=client_id, client_secret=client_secret)

# Interacting with Instructor Endpoints
print('************** Instructor **************')
print("Accessing instructor endpoints")
ins_client = api_client.instructor(course_id=course_id)

# Example: Get role members with the role 'instructor'
print("Role members:")
resp = ins_client.role_members(rolename='instructor')
print(resp)


# Interacting with Course Endpoints
print('************** Courses **************')
print("Accessing course endpoints")
course_client = api_client.course(course_id=course_id)

# Example: Get course details
print("Course details:")
resp = course_client.get_course_details()
print(resp._content)
