import requests
import json

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.core.paginator import Paginator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from ratelimit.decorators import ratelimit
from django.utils.encoding import force_bytes, force_str

from .models import ContactMessages, Schedule, Movie
from .utils import next_days, today
from .forms import SignupForm
from .token import account_activation_token


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('bookings')
        else:
            messages.success(request, message='There was an error logging in')
            HttpResponse('Invalid credentials')
            return redirect('login_page')
    else:
        return render(request, 'login_page.html')


def homepage(request):
    return render(request, 'homepage.html')


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        print('Method was POST')
        if form.is_valid():
            print('Form was valid')
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            message = render_to_string('acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            activation_form_data = {
                'name': request.POST['username'],
                'phone': 1234567,
                'city': 'Cluj',
                'cinema': 'Cinema X',
                'email': request.POST['email'],
                'subject': "activation link as been sent to your email address",
                'message': message,
            }
            send_contact_email(user_data=activation_form_data)
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


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
    return render(request, template_name='bookings.html', context={'bookings': schedules})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@ratelimit(key='ip', rate='2/h')
def fetch_playing_movies(request):
    next_7_days = next_days(7)
    schedules = Schedule.objects.filter(schedule_time__range=[today(), next_7_days])
    paginator = Paginator(schedules, per_page=5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, template_name="now_playing.html",
                  context={"page_obj": page_obj})


def send_contact_email(user_data: dict) -> None:
    response = requests.post(
        url=settings.SENDIN_BLUE["api_url"],
        headers={
            'content-type': 'application/json',
            'api-key': f'{settings.SENDIN_BLUE["api_key"]}'
        },
        data=json.dumps({
            "sender": {
              "name": "Cinema X ",
              "email": f"{user_data['email'].split('@')[0]}@test.com",
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
    print(f'Successfuly sent email with response: {response.content}')
