from django.urls import path, include
from rest_framework.routers import DefaultRouter

from storage.views.file_link import UniqueLinkView
from storage.views.files import FilesViewSet


app_name = 'storage'

router = DefaultRouter()
router.register(r'', FilesViewSet, 'files')

urlpatterns = [
    path('files/', include(router.urls)),
    path('files/link/', UniqueLinkView.as_view(), name='get-link'),
]
