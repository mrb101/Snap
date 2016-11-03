from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['category', 'starts', 'duration']


class BookingConfirmationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_confirmed',]


class CarDeliveryForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car_deliverd',]


class BookingClosingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car_returned', 'fees_paid']
