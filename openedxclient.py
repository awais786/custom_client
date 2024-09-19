"""
This module contains client classes for interacting with Open edX platform APIs, including
Instructor and Course APIs. These clients provide a structured way to interact with various
endpoints related to course and instructor operations using the OpenEdxClient as the base API client.
"""

import json
import requests
import inspect

# defines JSON configuration with more readable names as keys.
# The json will be external files.

INSTRUCTOR_RESOURCES = {
    "role_members": {
        "endpoint": "/courses/{course_id}/instructor/api/list_course_role_members",
        "method": "POST",
        "require_params": ['rolename']
    },
    "anonymous_ids": {
        "endpoint": "/courses/{course_id}/instructor/api/get_anon_ids",
        "method": "POST",
    },
    "student_progress_url": {
        "endpoint": "/courses/{course_id}/instructor/api/get_student_progress_url",
        "method": "POST",
        "require_params": ['unique_student_identifier']
    },
    "register_and_enroll": {
        "endpoint": "/courses/{course_id}/instructor/api/register_and_enroll_students",
        "method": "POST",
    },
    "entrance_exam_tasks": {
        "endpoint": "/courses/{course_id}/instructor/api/list_entrance_exam_instructor_tasks",
        "method": "POST",
        "require_params": ['unique_student_identifier']
    },
    "email_content": {
        "endpoint": "/courses/{course_id}/instructor/api/list_email_content",
        "method": "POST",
    },
    # "all_tasks": {
    #     "endpoint": "/courses/{course_id}/instructor/api/list_instructor_tasks",
    #     "method": "POST",
    #     "optional_params": ['unique_student_identifier', 'problem_location_str']
    # },
}

COURSE_RESOURCES = {
    "get_course_details": {
        "endpoint": "/api/courses/v1/courses/{course_id}",
        "method": "GET"
    },
}


# Generator to lazily generate the endpoint with the course_id
def endpoint_generator(url):
    yield url


class BaseClient:
    """
    BaseClient(api_client, course_id, resources)
    A base class for generating dynamic methods for API operations.
    """

    def __init__(self, api_client, course_id, resources):
        self.api_client = api_client
        self.course_id = course_id
        for operation, config in resources.items():
            setattr(self, operation, self.api_client.generate_method({
                'endpoint': config['endpoint'].format(course_id=self.course_id),
                'method': config['method']
            }))


class InstructorClient(BaseClient):
    """
    A client for performing instructor-related operations.
    This client inherits from BaseClient and automatically generates methods for interacting
    with instructor endpoints defined in the INSTRUCTOR_RESOURCES configuration.
    """

    def __init__(self, api_client, course_id):
        super().__init__(api_client, course_id, INSTRUCTOR_RESOURCES)


class CourseClient(BaseClient):
    """
    A client for performing course-related operations.
    This client inherits from BaseClient and automatically generates methods for interacting
    with course endpoints defined in the COURSE_RESOURCES configuration.
    """

    def __init__(self, api_client, course_id):
        super().__init__(api_client, course_id, COURSE_RESOURCES)


class OpenEdxClient:
    """
    A client for making HTTP requests to the Open edX platform APIs.
    This class provides generic methods for sending GET and POST requests to various endpoints
    within the Open edX platform. It serves as the base client that can be extended by more specific
    clients, such as `InstructorClient` and `CourseClient`, to interact with different API resources.
    """

    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.accesstoken = None

    def authenticate(self, client_id, client_secret):
        """
        Authenticates a user and retrieves a JWT token.
        """
        response = requests.get(f"{self.base_url}/csrf/api/v1/token", headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.headers['X-CSRFToken'] = data.get('csrfToken')

        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
            'token_type': 'jwt'
        }
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        response = requests.post(f"{self.base_url}/oauth2/access_token", headers=self.headers, data=payload)

        if response.status_code == 200:
            data = response.json()
            self.accesstoken = data.get('access_token')
            self.headers['Authorization'] = f"JWT {self.accesstoken}"
            self.headers['Content-Type'] = 'application/json'
            print('Authentication works!!!')
            return self
        else:
            print(f"Authentication failed: {response.status_code} {response.text}")
            return None

    def get(self, endpoint, data=None):
        """Send a GET request."""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=data)
        return response

    def post(self, endpoint, data=None):
        """Send a POST request."""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        return response

    def generate_method(self, resource_config):
        """
        Generate a method based on the resource configuration (endpoint, method).
        """
        api_endpoint = resource_config.get('endpoint')
        method = resource_config.get('method')
        required_params = resource_config.get('require_params', [])

        def api_call(*args, **kwargs):
            missing_params = [param for param in required_params if param not in kwargs]
            if missing_params:
                raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

            if not api_endpoint or not method:
                raise ValueError(f"Invalid resource configuration: {resource_config}")

            # Use the generator to get the endpoint
            endpoint_gen = endpoint_generator(api_endpoint)
            endpoint = next(endpoint_gen)  # Generate the endpoint URL

            data = kwargs

            # Handle method-specific logic
            if method == 'GET':
                return self.get(endpoint, data=data)
            elif method == 'POST':
                return self.post(endpoint, data=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

        signature = inspect.Signature(
            parameters=[
                inspect.Parameter(param, inspect.Parameter.KEYWORD_ONLY) for param in required_params
            ]
        )
        api_call.__signature__ = signature
        api_call.__doc__ = f"Automatically generated method for {method} {api_endpoint}"

        return api_call

    def instructor(self, course_id):
        """
        Method to return an instance of InstructorClient.
        """
        return InstructorClient(self, course_id)

    def course(self, course_id=None):
        """Returns an instance of CourseClient."""
        return CourseClient(self, course_id)
