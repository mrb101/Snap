from django.shortcuts import render


def home(request):
    template = 'main/index.html'
    if request.method == "POST":
        print("hello")
    context = {}
    return render(request, template, context)
