from django.shortcuts import render

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'main/home.html'


class AboutView(TemplateView):
    template_name = 'templates/main/about.html'


class Contact(TemplateView):
    template_name = 'templates/main/contact.html'
