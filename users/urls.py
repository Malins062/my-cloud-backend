from django.urls import path
from users.views.auth import RegistrationView, LogoutView, LoginView
from users.views.user import ProfileView, ChangePasswordView
from users.views.users import UsersListView

app_name = 'users'

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),

    path('users/', UsersListView.as_view(), name='users-list'),

    path('user/reg/', RegistrationView.as_view(), name='user-reg'),
    path('user/change-pswd/', ChangePasswordView.as_view(), name='user-change-pswd'),
    path('user/profile/', ProfileView.as_view(), name='profile'),
]
