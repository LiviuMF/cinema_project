from django.urls import path
from . import views
import re


urlpatterns = [
    path('login/', views.login_user, name='login_page'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.signup, name='register_page'),
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
]