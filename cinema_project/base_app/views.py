from django.core.paginator import Paginator
from django.shortcuts import render

from ratelimit.decorators import ratelimit

from .models import ContactMessages, Schedule
from .utils import today, send_contact_email, next_days


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


def bookings(request):
    schedules = Schedule.objects.filter(schedule_time__gte=today()).order_by('schedule_time')
    print(schedules)
    return render(request, template_name='bookings.html', context={'bookings': schedules})


@ratelimit(key='ip', rate='2/h')
def fetch_playing_movies(request):
    next_7_days = next_days(7)
    schedules = Schedule.objects.filter(schedule_time__range=[today(), next_7_days])
    paginator = Paginator(schedules, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, template_name="now_playing.html",
                  context={"page_obj": page_obj})
