from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views.auth import LogoutView, LoginView
from users.views.user import RegistrationView, ProfileView, ChangePasswordView
from users.views.users import UsersViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'', UsersViewSet, 'users')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    path('users/', include(router.urls)),

    path('user/reg/', RegistrationView.as_view(), name='registration'),
    path('user/me/', ProfileView.as_view(), name='profile'),
    path('user/change-pswd/', ChangePasswordView.as_view(), name='change-password'),
]
