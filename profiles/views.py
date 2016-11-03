from django.shortcuts import render


def login(request):
    template = 'profiles/login.html'
    context = {}
    return render(request, template, context)


def register(request):
    template = 'profiles/register.html'
    context = {}
    return render(request, template, context)
