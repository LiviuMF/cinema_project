from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse

from ratelimit.decorators import ratelimit

from .models import ContactMessages, Schedule, Cinema, Seat, Hall, User, Reservation
from .utils import today, send_contact_email, next_days, fetch_from_csv


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
        send_contact_email(user_data=contact_context)
        contact_message = ContactMessages(**contact_context)
        contact_message.save()
        return render(request, template_name='contact.html',
                      context=contact_context)
    return render(request, template_name='contact.html')


@ratelimit(key='ip', rate='2/h')
def fetch_currently_playing_movies_page(request):
    next_7_days = next_days(7)
    schedules = Schedule.objects.filter(schedule_time__range=[today(), next_7_days])
    paginator = Paginator(schedules, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, template_name="now_playing.html",
                  context={"page_obj": page_obj})


def bookings_page(request):
    cinema_cities = list(set([cinema.city for cinema in Cinema.objects.all()]))
    cinema_cities.sort()
    selected_city = cinema_cities[0]
    if request.method == 'POST':
        if request.POST.get('selected_city'):
            selected_city = request.POST['selected_city']
            return redirect('city_filtered_page', selected_city)
    return render(request, template_name='bookings.html', context={'cinema_cities': cinema_cities,
                                                                   'selected_city': selected_city})


def city_filtered_page(request, selected_city):
    schedules_by_city = Schedule.objects.filter(schedule_time__range=[today(), next_days(7)])\
        .filter(hall__cinema__city__iexact=selected_city)
    cinema_names = list(set(schedule.hall.cinema.name for schedule in schedules_by_city))
    cinema_names.sort()
    selected_cinema = cinema_names[0]
    if request.method == 'POST':
        selected_cinema = request.POST['selected_cinema']
        cinema_names.pop(cinema_names.index(selected_cinema))
        cinema_names.insert(0, selected_cinema)
    schedules_by_city_and_cinema = Schedule.objects.filter(hall__cinema__city__iexact=selected_city) \
        .filter(hall__cinema__name__iexact=selected_cinema).filter(schedule_time__range=[today(), next_days(7)])
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
    reserved_seats = [reservation.seat for reservation in Reservation.objects.filter(schedule__id=schedule_id)]
    return render(request, template_name='seats_page.html', context={'schedule_id': schedule_object.pk,
                                                                     'schedule': schedule_object,
                                                                     'all_seats': all_seats,
                                                                     'reserved_seats': reserved_seats})


def reservation_page(request, schedule_id):
    if request.method == 'POST':
        seats = list(request.POST.keys())[1:]
        for seat in seats:
            reservation = Reservation(
                user=User.objects.get(username=request.user),
                schedule=Schedule.objects.get(pk=schedule_id),
                seat=Seat.objects.get(pk=seat)
            )
            reservation.save()
    return render(request, template_name='reservation_page.html', context={'reservation': reservation,
                                                                           'seats': seats})
