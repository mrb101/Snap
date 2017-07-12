from django import forms
from .models import Booking, Category


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['category', 'starts', 'duration', 'dropoff']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'starts': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
            'dropoff': forms.TextInput(attrs={'class': 'form-control'}),
        }


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
