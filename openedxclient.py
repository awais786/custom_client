"""
This module contains client classes for interacting with Open edX platform APIs, including
Instructor and Course APIs. These clients provide a structured way to interact with various
endpoints related to course and instructor operations using the OpenEdxClient as the base API client.
"""

import json
import requests
import inspect
import sys
import os
import yaml
import os
import json


def parse_file(file_path):
    # Check if the file exists
    if not os.path.exists(yaml_file):
        raise FileNotFoundError(f"File not found: {yaml_file}")

    try:
        # Load the YAML file
        with open(file_path, 'r', encoding='utf-8') as file:
            if file_path.endswith('.yaml') or file_path.endswith('.yml'):
                # Parse YAML file
                openapi_data = yaml.safe_load(file)
            elif file_path.endswith('.json'):
                # Parse JSON file
                openapi_data = json.load(file)
            else:
                raise ValueError("Unsupported file format. Only .yaml and .json are supported.")

        # Extract 'paths'
        paths = openapi_data.get('paths', {})
        if not paths:
            print("No 'paths' key found in the YAML file.")
            return []

        return paths

    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}")


def get_instructor_links(paths):
    # Parse instructor-related links with method types
    # Parse instructor-related links with method types and format them
    # Parse instructor-related links with method types and format them
    instructor_resources = {}
    for path, methods in paths.items():
        if path.startswith("/courses/{course_id}/instructor/"):
            for method, details in methods.items():
                # Extract the endpoint key (the part after /instructor/api/)
                path_segments = path.split('/')
                endpoint_key = path_segments[-1]  # The last segment (after /instructor/api/)

                # Create a resource dictionary for the path
                resource = {
                    "endpoint": path,
                    "method": method.upper(),  # Convert method to uppercase (e.g., POST, GET)
                }

                # Add 'require_params' if available from the details
                parameters = details.get("parameters", [])
                require_params = [param["name"] for param in parameters if param["in"] == "query"]
                if require_params:
                    resource["require_params"] = require_params

                # Add this resource to the dictionary using the extracted endpoint key
                instructor_resources[endpoint_key] = resource

    return instructor_resources


yaml_file = "nov_28.yaml"
data = parse_file(yaml_file)

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

    def __init__(self, api_client, file_path, course_id):
        data = parse_file(file_path)
        self.instructor_links = get_instructor_links(data)

        # Generate a dynamic docstring for the client
        endpoint_docs = "\n".join([
            f"- `{key}`: {value['method']} {value['endpoint']}"
            for key, value in self.instructor_links.items()
        ])
        self.__doc__ += f"\n\nAvailable Endpoints:\n{endpoint_docs}"
        super().__init__(api_client, course_id, self.instructor_links)


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

    def instructor(self, file_path, course_id):
        """
        Method to return an instance of InstructorClient.
        """
        return InstructorClient(self, file_path, course_id)

    def course(self, course_id=None):
        """Returns an instance of CourseClient."""
        return CourseClient(self, course_id)
