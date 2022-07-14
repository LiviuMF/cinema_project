import requests
import json

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.paginator import Paginator

from .models import ContactMessages, Schedule
from .utils import days_ago


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('homepage')
        else:
            messages.success(request, message='There was an error logging in')
            return redirect('login_page')
    else:
        return render(request, 'login_page.html')


def homepage(request):
    return render(request, 'homepage.html')


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration succsefull!"))
            return redirect('homepage.html')
        else:
            form = UserCreationForm()
    return render(request, 'register_page.html', context={'form': form})


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


def fetch_playing_movies(request):
    last_7_days = days_ago(7)
    schedules = Schedule.objects.filter(schedule_time__gte=last_7_days)
    paginator = Paginator(schedules, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, template_name="now_playing.html",
                  context={"page_obj": page_obj})


def send_contact_email(user_data) -> None:
    requests.post(
        url=settings.SENDIN_BLUE["api_url"],
        headers={
            'content-type': 'application/json',
            'api-key': f'{settings.SENDIN_BLUE["api_key"]}'
        },
        data=json.dumps({
            "sender": {
              "name": "Cinema X ",
              "email": f"{user_data['email'].split('@')[0]}@example.com"
            },
            "to": [
                {
                    "email": "liviu.m.farcas@gmail.com",
                    "name": "Cinema X HQ"
                }
            ],
            "subject": user_data['subject'] or 'Message from Cinema X website',
            "htmlContent":
                f"<html><head></head><body><p>Hello,"
                f"</p>Received a new email from {user_data['name']},"
                f"<p> message: {user_data['message']}</p>"
                f"<p>Other contact details:</p>"
                f"<p>Phone number: {user_data['phone']}</p>"
                f"<p>City: {user_data['city']}</p>"
                f"<p>Cinema: {user_data['cinema']}</p>"
                f"</body></html>"
        })
    )
