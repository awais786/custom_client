"""
This module contains client classes for interacting with Open edX platform APIs, including
Instructor and Course APIs. These clients provide a structured way to interact with various
endpoints related to course and instructor operations using the OpenEdxClient as the base API client.
"""
import datetime
import json
import jwt
import requests

# defines JSON configuration with more readable names as keys.
# Each key has the url of the endpoint and HTTP method.

INSTRUCTOR_RESOURCES = {
    "tasks": {
        "endpoint": "/courses/{course_id}/instructor/api/list_instructor_tasks",
        "method": "POST"
    },
    "anonymous_ids": {
        "endpoint": "/courses/{course_id}/instructor/api/get_anon_ids",
        "method": "POST"
    },
    "student_progress_url": {
        "endpoint": "/courses/{course_id}/instructor/api/get_student_progress_url",
        "method": "POST"
    }
}

COURSE_RESOURCES = {
    "create_course": {
        "endpoint": "add_course",
        "method": "POST"
    },
    "get_course_info": {
        "endpoint": "get_course_details",
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
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, data=None, headers=None):
        """Send a GET request."""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=headers, params=data)
        return response

    def post(self, endpoint, data=None, headers=None):
        """Send a POST request."""
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response

    def generate_method(self, resource_config):
        """
        Generate a method based on the resource configuration (endpoint, method).
        """

        def api_call(*args, **kwargs):
            api_endpoint = resource_config.get('endpoint')
            method = resource_config.get('method')

            if not api_endpoint or not method:
                raise ValueError(f"Invalid resource configuration: {resource_config}")

            # Use the generator to get the endpoint
            endpoint_gen = endpoint_generator(api_endpoint)
            endpoint = next(endpoint_gen)  # Generate the endpoint URL

            headers = kwargs.get('headers', {})
            data = kwargs.get('data', {})

            # Handle method-specific logic
            if method == 'GET':
                return self.get(endpoint, data=data, headers=headers)
            elif method == 'POST':
                return self.post(endpoint, data=data, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

        return api_call

    def instructor(self, course_id):
        """
        Method to return an instance of InstructorClient.
        """
        return InstructorClient(self, course_id)

    def course(self, course_id=None):
        """Returns an instance of CourseClient."""
        return CourseClient(self, course_id)

