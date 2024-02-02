import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({
        "message": "csrf cookie set"
    })


@api_view(['POST',])
@permission_classes((AllowAny,))
def login_view(request):
    """
    POST API for login
    """
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    if username is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter username"
            }
        }, status=400)
    elif password is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter password"
            }
        }, status=400)

    # authentication user
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"success": "User has been logged in"})
    return JsonResponse(
        {"errors": "Invalid credentials"},
        status=400,
    )

# @require_POST
# def login_view(request):
#     data = json.loads(request.body)
#     username = data.get('username')
#     password = data.get('password')
#
#     if username is None or password is None:
#         return JsonResponse({
#             "message": "Please enter both email and password"
#         }, status=400)
#
#     user = authenticate(username=username, password=password)
#
#     if user is not None:
#         login(request, user)
#
#         return JsonResponse({
#             "message": "success",
#         })
#
#     return JsonResponse(
#         {
#             "message": "invalid credentials"
#         }, status=400
#     )
#

@require_POST
def logout_view(request):
    logout(request)

    return JsonResponse({
        "message": 'logout',
    })


def me_view(request):
    data = request.user

    return JsonResponse({
        "username": data.username,
        "isAdmin": data.is_staff,
    })