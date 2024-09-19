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