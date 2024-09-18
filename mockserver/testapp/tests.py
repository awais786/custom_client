from django.test import TestCase

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from openedxclient import OpenEdxClient


class OpenEdxClientTests(TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:8000"
        self.course_id = "course-v1:edx+cs222+2311"
        edx_client = OpenEdxClient(self.base_url)
        api_client = edx_client.authenticate(client_id="test_client", client_secret="test_secret")
        self.assertIsInstance(api_client, OpenEdxClient)
        self.insructor_client = api_client.instructor(course_id=self.course_id)
        self.unique_student_identifier = 'student@example.com'
        self.course_client = api_client.course(course_id=self.course_id)

    def test_instructor_endpoints(self):
        response = self.insructor_client.role_members(rolename='data_researcher')
        self.assertEqual(response.status_code, 200)
        self.assertIn('data_researcher', response.json()['data'])

    def test_student_progress_url(self):
        response = self.insructor_client.student_progress_url(unique_student_identifier='student@example.com')

        expected_data = {
            'course_id': str(self.course_id),
            'progress_url': f'/courses/{self.course_id}/progress/101/'
        }
        # {"course_id": "course-v1:edx+cs222+2015_t5", "progress_url": "/courses/course-v1:edx+cs222+2015_t5/progress/8/"}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_data, response.json()['data'])

    def test_instructor_endpoints(self):
        response = self.course_client.get_course_details()
        self.assertEqual(response.status_code, 200)
        self.assertIn('blocks_url', response.json()['data'])
