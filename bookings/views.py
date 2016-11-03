from django.shortcuts import render
from django.http import HttpResponse

import json
from datetime import datetime

from cars.models import Category

from .models import Booking
from .forms import (
    BookingForm,
    BookingConfirmationForm,
    CarDeliveryForm,
    BookingClosingForm,
)


def bookings(request):
    template = 'bookings/list.html'
    bookings = Booking.objects.all()
    context = {'bookings': bookings}
    return render(request, template, context)


def booking(request, id):
    template = 'bookings/show.html'
    booking = Booking.objects.get(id=id)
    context = {'booking': bookings}
    return render(request, template, context)


def car_booking(request):
    template = 'bookings/form.html'
    form = BookingForm(request.POST)
    if request.method == 'POST':
        category_number = request.POST.get('category')
        category = Category.objects.get(id=category_number)
        starts = request.POST.get('starts')
        print(starts)
        duration = request.POST.get('duration')
        booking = Booking()
        booking.customer = request.user
        booking.category = category
        booking.starts = datetime.strptime(starts, '%x %X')
        booking.duration = duration
        booking.save()
        return HttpResponse(json.dumps({
            'type': 'S01',
            'msg': 'You order has been submited.',
            'category': booking.category,
            'starts': booking.starts,
        }))
    context = {'form': form}
    return render(request, template, context)


def confirm_booking(request, id):
    template = 'bookings/form.html'
    form = BookingConfirmationForm(request.POST)
    booking = Booking.objects.get(id=id)
    if request.method == 'POST':
        booking.booking_confirmed = request.POST.get('checked')
        booking.save()
        return HttpResponse(json.dumps({
            'type': 'S01',
            'msg': 'You have confirmed booking number {0}'.format(booking_number),
            'starts': booking.starts,
            'duration': booking.duration,
            'address': booking.dropoff,
            'customer': booking.customer,
            'phone': booking.customer.mobile,
        }))
    context = {'form': form}
    return render(request, template, context)


def car_delivery(request, id):
    template = 'bookings/form.html'
    form = CarDeliveryForm(request.POST)
    booking = Booking.objects.get(id=id)
    if request.method == 'POST':
        booking.car_deliverd = request.POST.get('checked')
        booking.save()
        return HttpResponse(json.dumps({
            'type': 'S01',
            'msg': 'Thank you, Pick up time for the car is on {0}'.format(booking.rentalends),
            'fees': 'The total should be{0}'.format(booking.category.price)
        }))
    context = {'form': form}
    return render(request, template, context)


def car_return(request, id):
    template = 'bookings/form.html'
    form = BookingClosingForm(request.POST)
    booking = Booking.objects.get(id=id)
    if request.method == 'POST':
        booking.car_returned = request.POST.get('returned')
        booking.fees_paid = request.POST.get('paid')
        booking.save()
        return HttpResponse(json.dumps({
            'type': 'S01',
            'amount': booking.category.price,
            'msg': 'Thank you',
        }))
    context = {'form': form}
    return render(request, template, context)