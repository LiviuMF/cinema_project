from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from base_app.views import MovieViewSet


router = routers.DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cinema/', include('base_app.urls')),
    path('members/', include('members.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)