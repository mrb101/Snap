from django.shortcuts import render


def home(request):
    template = 'main/home.html'
    context = {}
    return render(request, template, context)
