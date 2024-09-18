from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def csrf_token_view(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})


@csrf_exempt
def oauth_token(request):
    if request.method == "POST":
        # Get data from the request
        grant_type = request.POST.get('grant_type')
        token_type = request.POST.get('token_type')

        # Check if grant_type is correct
        if grant_type == 'client_credentials':
            return JsonResponse({
                'access_token': 'mocked-access-token',
                'token_type': token_type
            })

        return JsonResponse({'error': 'unsupported_grant_type'}, status=400)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def list_course_role_members(request, course_id):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        rolename = data.get('rolename')
        if not rolename:
            return JsonResponse({'error': rolename}, status=400)

        resp_data = {
            "course_id": course_id,
            "data_researcher": [
                {
                    "username": "admin",
                    "email": "admin@example.com",
                    "first_name": "abc",
                    "last_name": "qdd"
                },
                {
                    "username": "login_service_user",
                    "email": "login_service_user@fake.email",
                    "first_name": "",
                    "last_name": ""
                }
            ]
        }

        return JsonResponse({
            'status': 'success',
            'data': resp_data
        })

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def get_student_progress_url(request, course_id):
    if request.method == "POST":

        data = json.loads(request.body.decode('utf-8'))
        unique_student_identifier = data.get('unique_student_identifier')
        if not unique_student_identifier:
            return JsonResponse({'error': unique_student_identifier}, status=400)

        data = {
            'course_id': course_id,
            'progress_url': f'/courses/{course_id}/progress/101/'
        }

        return JsonResponse({
            'status': 'success',
            'course_id': course_id,  # Capture the course_id
            'data': data  # Return all POST data
        })

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
