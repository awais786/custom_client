import unittest
from openedxclient import OpenEdxClient, InstructorClient
from unittest.mock import patch, MagicMock

class TestOpenEdxClient(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://example.com"
        self.course_id = "course-v1:edX+DemoX+T2024"
        self.edx_client = OpenEdxClient(self.base_url)
        self.client_id = 'test'
        self.client_secret = 'sec'

    def test_instructor_client_creation(self):
        # Test creating an InstructorClient instance
        instructor_client = self.edx_client.instructor(self.course_id)
        # Assert that the returned client is an instance of InstructorClient
        self.assertIsInstance(instructor_client, InstructorClient)

    @patch('openedxclient.requests.post')
    @patch('openedxclient.requests.get')
    def test_authenticate(self, mock_get, mock_post):
        # Mock CSRF token request
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {'csrfToken': 'fake_csrf_token'})

        # Mock access token request
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {'access_token': 'fake_access_token'})

        result = self.edx_client.authenticate(self.client_id, self.client_secret)

        # Assert CSRF token is set
        self.assertEqual(self.edx_client.headers['X-CSRFToken'], 'fake_csrf_token')

        # Assert Access token is set in the Authorization header
        self.assertEqual(self.edx_client.headers['Authorization'], 'JWT fake_access_token')
        self.assertIsNotNone(result)  # Check if the client is returned

    @patch('requests.post')
    def test_role_members_endpoint(self, mock_post):
        base_url = "http://example.com"
        course_id = "course-v1:edX+DemoX+T2024"
        edx_client = OpenEdxClient(base_url)
        instructor_client = edx_client.instructor(course_id)

        # Mock the response from the POST request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Call the dynamically generated method for role_members
        response = instructor_client.role_members(data={'rolename': 'instructor'})

        # Assert that the request was made with correct endpoint and method
        mock_post.assert_called_once_with(
            f"{base_url}/courses/{course_id}/instructor/api/list_course_role_members",
            headers=edx_client.headers,
            data='{"rolename": "instructor"}'  # Ensure payload was correctly passed
        )
        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_anonymous_ids_endpoint(self, mock_post):
        base_url = "http://example.com"
        course_id = "course-v1:edX+DemoX+T2024"
        edx_client = OpenEdxClient(base_url)
        instructor_client = edx_client.instructor(course_id)

        # Mock the response from the POST request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Call the dynamically generated method for anonymous_ids
        response = instructor_client.anonymous_ids()

        # Assert that the request was made with correct endpoint and method
        mock_post.assert_called_once_with(
            f"{base_url}/courses/{course_id}/instructor/api/get_anon_ids",
            headers=edx_client.headers,
            data='{}'  # No additional data sent
        )
        self.assertEqual(response.status_code, 200)

    @patch('requests.post')
    def test_student_progress_url_endpoint(self, mock_post):
        base_url = "http://example.com"
        course_id = "course-v1:edX+DemoX+T2024"
        edx_client = OpenEdxClient(base_url)
        instructor_client = edx_client.instructor(course_id)

        # Mock the response from the POST request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Call the dynamically generated method for student_progress_url
        response = instructor_client.student_progress_url(data={'unique_student_identifier': '12345'})

        # Assert that the request was made with correct endpoint and method
        mock_post.assert_called_once_with(
            f"{base_url}/courses/{course_id}/instructor/api/get_student_progress_url",
            headers=edx_client.headers,
            data='{"unique_student_identifier": "12345"}'
        )
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
