"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from main import views as main_views
from profiles import views as profiles_views
from bookings import urls as bookings_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^booking/', include(bookings_urls, namespace="booking")),
    url(r'^login/$', profiles_views.signin, name='login'),
    url(r'^logout/$', profiles_views.signout, name='logout'),
    url(r'^register/$', profiles_views.register, name='register'),

    url(r'^$', main_views.HomeView.as_view(), name='home'),
]
