from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_user, name='login_page'),
    path('', views.homepage, name='homepage'),
    path('register/', views.register_user, name='register_page'),
    path('contact/', views.contact_page, name='contact')
]
