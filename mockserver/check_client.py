import sys
import os

# Add the parent directory of 'mockserver' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from openedxclient import OpenEdxClient
base_url='http://localhost:8000/'
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
print('************** Courses **************')
print("Accessing course endpoints")
course_client = api_client.course(course_id=course_id)
resp = course_client.get_course_details()
print("course details:")
print(resp._content)
print('************** All endpoints runs successfully **************')
