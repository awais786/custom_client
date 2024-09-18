from django.urls import re_path
from . import views

# Define the regex pattern for the course ID
COURSE_KEY_PATTERN = r'(?P<course_key_string>[^/+]+(/|\+)[^/+]+(/|\+)[^/?]+)'
COURSE_ID_PATTERN = COURSE_KEY_PATTERN.replace('course_key_string', 'course_id')

urlpatterns = [
    # URL pattern to match the instructor API endpoint
    re_path(
        rf'^courses/{COURSE_ID_PATTERN}/instructor/api/list_course_role_members/?$',
        views.list_course_role_members,
        name='list-course-role-members'
    ),
    re_path(
        rf'^courses/{COURSE_ID_PATTERN}/instructor/api/get_student_progress_url/?$',
        views.get_student_progress_url,
        name='get-student-progress-url'
    ),
    re_path(
        r'^oauth2/access_token/?$',
        views.oauth_token,
        name='oauth-token'
    ),
    re_path(
        r'^csrf/api/v1/token/?$',
        views.csrf_token_view,
        name='csrf-token'
    ),
]
