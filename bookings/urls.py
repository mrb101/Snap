from django.conf.urls import url

from .views import (
    CreateBooking,
    BookingDetails,
    ConfirmBooking,
    BookingDelivered,
    BookingReturn,
    BookingFees,
    BookingClosed,
)


urlpatterns = [
    url(r'^create/$', CreateBooking.as_view(), name='create_booking'),
    url(r'^(?P<booking_number>[-\w]+)/$', BookingDetails.as_view(), name="details_booking"),
    url(r'^(?P<booking_number>[-\w]+)/confirm/$', ConfirmBooking.as_view(), name="confirm_booking"),
    url(r'^(?P<booking_number>[-\w]+)/delivered/$', BookingDelivered.as_view(), name="car_delivered"),
    url(r'^(?P<booking_number>[-\w]+)/return/$', BookingReturn.as_view(), name="car_return"),
    url(r'^(?P<booking_number>[-\w]+)/fees/$', BookingFees.as_view(), name="booking_fees"),
    url(r'^(?P<booking_number>[-\w]+)/closed/$', BookingClosed.as_view(), name="booking_closed"),
]
