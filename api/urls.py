from django.urls import path
from . import views


urlpatterns = [
    path('currently_playing/', views.currently_playing),
    path('currently_playing_with_schedule/', views.currently_playing_with_schedule),
    path('movies/', views.MovieSearchView.as_view()),
    path('create-hall/', views.create_hall),
    path('update-hall/', views.update_hall),
    path('create-movie/', views.create_movie),
    path('update-movie/', views.update_movie),
]
