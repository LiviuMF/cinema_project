from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('contact/', views.contact_page, name='contact'),
    path('now_playing/', views.fetch_currently_playing_movies_page, name='now_playing'),
    path('bookings/', views.bookings_page, name='bookings'),
    path('bookings/city/<str:selected_city>', views.city_filtered_page, name='city_filtered_page'),
    path('bookings/seats/<str:schedule_id>', views.seats_page, name='seats_page'),
    path('bookings/reservation_page/<str:schedule_id>', views.reservation_page, name='reservation_page'),
    path('movie-page/<str:schedule_id>', views.movie_page, name='movie_page'),
    path('my-reservations/', views.my_reservations_page, name='my_reservations'),
    path('download_my_reservations/', views.download_my_reservations_csv, name='download_my_reservations'),
]
