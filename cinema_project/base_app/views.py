from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


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
