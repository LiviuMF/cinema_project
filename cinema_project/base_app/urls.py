from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('contact/', views.contact_page, name='contact'),
    path('now_playing/', views.fetch_playing_movies, name='now_playing'),
    path('bookings/', views.bookings, name='bookings'),
]
