from django.urls import path, include

from users.views.auth import RegistrationView
from users.views.auth2 import login_view, logout_view, get_csrf_token
from users.views.profile import ProfileView, ChangePasswordView

app_name = 'users'

urlpatterns = [
    path('auth/login/', login_view, name='auth-login'),
    path('auth/logout/', logout_view, name='auth-logout'),
    path('auth/get_csrf/', get_csrf_token, name='auth-csrf'),

    path('user/reg/', RegistrationView.as_view(), name='user-reg'),
    path('user/change-pswd/', ChangePasswordView.as_view(), name='user-change-pswd'),
    path('user/profile/', ProfileView.as_view(), name='profile'),
]
