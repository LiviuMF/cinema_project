from django.urls import path, include
from . import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('currently_playing/', views.currently_playing),
    path('currently_playing_with_schedule/', views.currently_playing_with_schedule),
    path('movies/', views.MovieSearchView.as_view()),
    path('create-hall/', views.create_hall),
    path('update-hall/', views.update_hall),
    path('create-movie/', views.create_movie),
    path('update-movie/', views.update_movie),
    path('create-schedule/', views.create_schedule),
    path('update-schedule/', views.update_schedule),
    path('confirm-reservation/', views.confirm_reservation),
    path('reservations/', views.ReservationListCreate.as_view()),
    path('reservations/<int:pk>/update/', views.ReservationListUpdate.as_view()),
]
