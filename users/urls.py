from django.urls import path
from users.views.auth import LogoutView, LoginView
from users.views.user import RegistrationView, ProfileView, ChangePasswordView
from users.views.users import UsersListView

app_name = 'users'

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),

    path('users/', UsersListView.as_view(), name='users-list'),

    path('user/', RegistrationView.as_view(), name='user-registration'),
    path('user/change-pswd/', ChangePasswordView.as_view(), name='user-change-password'),
    path('user/profile/', ProfileView.as_view(), name='profile'),
]
