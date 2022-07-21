from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cinema/', include('base_app.urls')),
    path('members/', include('login.urls')),
    path('members/', include('django.contrib.auth.urls')),
]