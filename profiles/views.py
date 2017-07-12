from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


def signin(request):
    template = 'profiles/login.html'
    form =  AuthenticationForm(request.POST)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(request.GET.get('next') or 'booking:create_booking')
            else:
                return redirect('login')
        else:
            return redirect('login')
    context = {'form': form}
    return render(request, template, context)


def register(request):
    template = 'profiles/register.html'
    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            pass


def signout(request):
    logout(request)
    return redirect('home')
