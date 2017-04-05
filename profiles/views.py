from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

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
                return redirect(request.GET.get('next') or 'new-booking')
            else:
                return redirect('login')
        else:
            return redirect('login')
    context = {'form': form}
    return render(request, template, context)


def register(request):
    if request.method == "POST":
        print("hello from post")


def signout(request):
    logout(request)
    return redirect('login')
