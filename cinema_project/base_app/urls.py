from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('contact/', views.contact_page, name='contact'),
    path('now-playing/', views.fetch_currently_playing_movies_page, name='now_playing'),
    path('bookings/', views.bookings_page, name='bookings'),
    path('bookings/city/<str:selected_city>', views.city_filtered_page, name='city_filtered_page'),
    path('bookings/seats/<str:schedule_id>', views.seats_page, name='seats_page'),
    path('bookings/reservation-page/<str:schedule_id>', views.reservation_page, name='reservation_page'),
    path('movie-page/<str:schedule_id>', views.movie_page, name='movie_page'),
    path('my-reservations/', views.my_reservations_page, name='my_reservations'),
    path('download-my-reservations/', views.download_my_reservations_csv, name='download_my_reservations'),
    path('reservation-confirmation/<token>', views.confirm_reservation, name='reservation_confirmation'),
]
