from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls'), name='api'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
