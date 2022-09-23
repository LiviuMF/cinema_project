from django.urls import path, include
from . import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('currently_playing/', views.currently_playing),
    path('currently_playing_with_schedule/', views.currently_playing_with_schedule),
    path('movie/<int:pk>/', views.MovieListCreate.as_view()),
    path('movies/', views.MovieListCreate.as_view()),
    path('hall/<int:pk>/', views.HallListCreateUpdate.as_view()),
    path('halls/', views.HallListCreateUpdate.as_view()),
    path('schedule/<int:pk>/', views.ScheduleListCreateUpdate.as_view()),
    path('schedules/', views.ScheduleListCreateUpdate.as_view()),
    path('reservation/<int:pk>/', views.ReservationListCreateUpdate.as_view()),
    path('reservations/', views.ReservationListCreateUpdate.as_view()),
    path('seat/<int:pk>/', views.SeatUpdate.as_view()),
]
