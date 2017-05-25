from django.conf.urls import url

from .views import (
    bookings,
    car_booking,
    confirm_booking,
    car_delivery,
    car_return,
)


urlpatterns = [
    url(r'^$', bookings, name='booking'),
    url(r'^new/$', car_booking, name='new-booking'),
    url(r'^confirm/$', confirm_booking, name='confirm-booking'),
    url(r'^deliverd/$', car_delivery, name='confirm-delivery'),
    url(r'^retunrd/$', car_return, name='confirm-returned'),
]
