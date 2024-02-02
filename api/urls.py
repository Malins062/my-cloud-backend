from django.urls import path, include
from api.spectacular.urls import urlpatterns as spectacular_doc_urls
from users.urls import urlpatterns as user_urls
from storage.urls import urlpatterns as storage_urls


app_name = 'api'

urlpatterns = [
    # path('auth/', include('rest_framework.urls', namespace='rest_framework'), name='auth'),
]

urlpatterns += spectacular_doc_urls
urlpatterns += user_urls
urlpatterns += storage_urls
