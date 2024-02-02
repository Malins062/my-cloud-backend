from django.urls import path, include

from users.views.auth import login_view, logout_view, get_csrf_token

app_name = 'users'

urlpatterns = [
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view),
    path('auth/get_csrf/', get_csrf_token),
]
