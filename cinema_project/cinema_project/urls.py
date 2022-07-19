from django.contrib import admin
from django.urls import path, include
import cinema_project


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base_app.urls')),
    path('', include('django.contrib.auth.urls')),
]
