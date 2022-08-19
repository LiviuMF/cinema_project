import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions

from ratelimit.decorators import ratelimit

from .models import ContactMessages, Schedule, Cinema, Seat, User, Reservation
from cinema_project.utils import today, send_email, next_days
from .serializers import MovieSerializer
from .token import reservation_confirmation


def homepage(request):
    return render(request, 'homepage.html')


def contact_page(request):
    if request.method == 'POST':
        contact_context = {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'city': request.POST['city'],
            'phone': request.POST['phone'],
            'cinema': request.POST['cinema'],
            'subject': request.POST['subject'],
            'message': request.POST['message'],
        }
        send_email(from_email=contact_context['email'],
                   subject=contact_context['subject'],
                   html_content=f"<p> Cinema: {contact_context['cinema']} </p>"
                                f"<p> City: {contact_context['city']}</p>"
                                f"<p> Message: {contact_context['message']} </p>"
                                f"<br><p> Contact Details:</p>"
                                f"<p> Name: {contact_context['name']}</p>"
                                f"<p> Phone: {contact_context['phone']}</p>",
                   )
        contact_message = ContactMessages(**contact_context)
        contact_message.save()
        return render(request, template_name='contact.html',
                      context=contact_context)
    return render(request, template_name='contact.html')


@ratelimit(key='ip', rate='100/h', block=True)
def fetch_currently_playing_movies_page(request):
    next_7_days = next_days(7)
    schedules = Schedule.objects.filter(schedule_time__range=[today(), next_7_days])
    paginator = Paginator(schedules, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, template_name="now_playing.html",
                  context={"page_obj": page_obj})


def bookings_page(request):
    cinema_cities = Cinema.objects.values_list('city', flat=True).order_by('city').distinct()
    selected_city = cinema_cities[0]
    if request.method == 'POST':
        if request.POST.get('selected_city'):
            selected_city = request.POST['selected_city']
            return redirect('city_filtered_page', selected_city)
    return render(request, template_name='bookings.html', context={'cinema_cities': cinema_cities,
                                                                   'selected_city': selected_city})


def city_filtered_page(request, selected_city):
    cinema_names = Schedule.objects.filter(
        hall__cinema__city=selected_city,
        schedule_time__range=[today(), next_days(7)]).values_list('hall__cinema__name', flat=True).distinct()
    selected_cinema = cinema_names[0]
    if request.method == 'POST':
        selected_cinema = request.POST['selected_cinema']
        cinema_names.pop(cinema_names.index(selected_cinema))
        cinema_names.insert(0, selected_cinema)
    schedules_by_city_and_cinema = Schedule.objects.filter(
        hall__cinema__city__iexact=selected_city,
        hall__cinema__name__iexact=selected_cinema,
        schedule_time__range=[today(), next_days(7)],
    )
    paginator = Paginator(schedules_by_city_and_cinema, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, template_name='city_filtered_page.html', context={'selected_city': selected_city,
                                                                             'cinema_names': cinema_names,
                                                                             'schedules_by_city_and_cinema': page_obj
                                                                             })


def seats_page(request, schedule_id):
    if not request.user.is_authenticated:
        return HttpResponse('You are not authenticated!')
    schedule_object = Schedule.objects.get(pk=schedule_id)
    all_seats = [schedule for schedule in schedule_object.hall.seat_set.all()]
    reserved_seats = Reservation.objects.filter(schedule__id=schedule_id).values_list('seat', flat=True)

    return render(request, template_name='seats_page.html', context={'schedule_id': schedule_object.pk,
                                                                     'schedule': schedule_object,
                                                                     'all_seats': all_seats,
                                                                     'reserved_seats': reserved_seats})


def reservation_page(request, schedule_id):
    schedule_object = Schedule.objects.get(pk=schedule_id)
    all_reservations = []
    if request.method == 'POST':
        seats = list(request.POST.keys())[1:]
        user = User.objects.get(username=request.user)
        for seat in seats:
            reservation = Reservation(
                user=user,
                schedule=schedule_object,
                seat=Seat.objects.get(pk=seat)
            )
            reservation.save()
            all_reservations.append(str(reservation.pk))
        reservation_param = "&".join(all_reservations)
        current_site = request.get_host()
        reservation_token = reservation_confirmation.make_token(user)
        send_email(
            from_email='cinema@cinemax.ro',
            subject='Confirmation on your reservation at Cinema X',
            html_content=f"<p>This is your confirmation from Cinema X:</p>"
                         f"<p>Reservation nr: {reservation.pk}</p>"
                         f"<p>Movie: {reservation.schedule.movie}</p>"
                         f"<p>Name: {user}</p>"
                         f"<p>Date/Time: {reservation.schedule.schedule_time}</p>"
                         f"<p>Seats: {seats}</p>"
                         f"<br>"
                         f"<p>Please confirm your registration at the following url:</p>"
                         f"<p>http://{current_site}/cinema/reservation-confirmation/{reservation_param}/{reservation_token}",
            to_email=user.email,
        )
        return render(request, template_name='reservation_page.html', context={'reservation': reservation,
                                                                               'seats': seats,
                                                                               'reservations': reservation_param})


def movie_page(request, schedule_id):
    schedule_object = Schedule.objects.get(pk=schedule_id)
    return render(request, template_name='movie_page.html', context={'schedule': schedule_object})


def my_reservations_page(request):
    return render(request, template_name='my_reservations.html')


def download_my_reservations_csv(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse('You Must Be Logged In To Download Reservations')
    my_reservations = User.objects.get(username=user.username).reservation_set.all()
    reservation_details = [
        {
            'user': user.username,
            'movie': reservation.schedule.movie.name,
            'duration': reservation.schedule.movie.duration,
            'date_time': reservation.schedule.schedule_time,
            'seats': reservation.seat.name,
        } for reservation in my_reservations
    ]
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{user.username}_reservations.csv"'},
    )
    writer = csv.DictWriter(response, fieldnames=list(reservation_details[0].keys()))
    writer.writeheader()
    writer.writerows(reservation_details)
    return response


def confirm_reservation(request, token, reservations):
    user = request.user
    if reservation_confirmation.check_token(user, token):
        for reservation in reservations.split('&'):
            reservation_object = Reservation.objects.get(pk=reservation)
            reservation_object.is_confirmed = True
            reservation_object.save()
        return HttpResponse('Thank you for confirming your reservation')
    return HttpResponse('The reservation link is not valid')


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.filter(schedule_time__range=[today(), next_days(7)])
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]
