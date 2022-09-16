from django.urls import path
from . import views


urlpatterns = [
    path('currently_playing/', views.currently_playing),
    path('currently_playing_with_schedule/', views.currently_playing_with_schedule),
    path('movies/', views.MovieSearchView.as_view())
]
