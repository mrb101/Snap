from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.contrib.auth.models import User

import json
from datetime import datetime, timedelta

from cars.models import Category

from .utils import send_sms_notification, send_email_notification

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


@login_required
def booking(request, id):
    confirm_template = 'bookings/booking_details.html'
    deliverd_template = 'bookings/car_deliverd.html'
    return_template  = 'bookings/car_return.html'
    closed_template = 'bookings/closed_booking.html'
    booking = Booking.objects.get(id=id)
    return_time = booking.duration + booking.starts
    context = {'booking': booking, 'return_time': return_time}
    if booking.car_returned == True:
        return render(request, closed_template, context)
    elif booking.car_deliverd == True:
        return render(request, return_template, context)
    elif booking.booking_confirmed == True :
        return render(request, deliverd_template, context)
    else:
        return render(request, confirm_template, context)


@login_required
def car_booking(request):
    template = 'bookings/form.html'
    form = BookingForm(request.POST)
    if request.method == 'POST':
        category_string = request.POST.get('category')
        print(category_string)
        category = Category.objects.get(concept=category_string)
        starts = request.POST.get('starts')
        duration = request.POST.get('duration')
        if duration == 'half':
            time = timedelta(hours=6)
        elif duration == 'day':
            time = timedelta(days=1)
        elif duration == 'week':
            time = timedelta(weeks=1)
        elif duration == 'month':
            time = timedelta(weeks=4)
        else:
            time = 'Something went wrong!'
        booking = Booking()
        booking.customer = request.user
        booking.category = category
        booking.starts = datetime.strptime(starts, '%Y-%m-%dT%H:%M')
        booking.duration = time
        booking.save()
        # get suppliers
        suppliers = User.objects.filter(profile__supplier=True)
        # loop over supplier and send sms
        for supplier in suppliers:
            phone = supplier.profile.phone
            send_sms_notification(str(phone), "go to 192.168.33.10:3000/book/{0} to accept booking".format(booking.id))
        return HttpResponse(json.dumps({
            'type': 'S01',
            'msg': 'You order has been submited.',
            'category': str(booking.category),
            'starts': str(booking.starts),
        }))
    context = {'form': form}
    return render(request, template, context)

@login_required
def confirm_booking(request, id):
    booking = Booking.objects.get(id=id)
    return_time = booking.duration + booking.starts
    if request.method == 'POST':
        if booking.booking_confirmed == True:
            return HttpResponse(json.dumps({
                'type': 'S02',
                'msg': 'Booking has been already confirmed',
            }))
        else:
            booking.booking_confirmed = True
            booking.supplier = request.user
            booking.save()
            customer = booking.customer
            phone = customer.profile.phone
            supplier = request.user
            booking = customer.customers.latest("updated")
            send_sms_notification(str(phone), "go to 192.168.33.10:3000/book/{0}  to confirm booking".format(booking.pk))
            return HttpResponse(json.dumps({
                'type': 'S01',
                'msg': 'You have confirmed booking number {0}'.format(booking.id),
                'starts': str(booking.starts),
                'duration': str(booking.duration),
                'address': str(booking.dropoff),
                'customer': str(booking.customer),
            }))


@login_required
def car_delivery(request, id):
    booking = Booking.objects.get(id=id)
    return_time = booking.duration + booking.starts
    if request.method == 'POST':
        if booking.car_deliverd == True:
            return HttpResponse(json.dumps({
                'type': 'S02',
                'msg': 'Car has  already been delivered',
            }))
        else:
            booking.car_deliverd = True
            booking.save()
            customer = booking.customer
            phone = customer.profile.phone
            send_sms_notification(str(phone), "go to 192.168.33.10:3000/book/{0}  to confirm car delivery".format(booking.pk))
            return HttpResponse(json.dumps({
                'type': 'S01',
                'msg': 'Thank you, Pick up time for the car is on {0}'.format(return_time),
            }))


@login_required
def car_return(request, id):
    booking = Booking.objects.get(id=id)
    if request.method == 'POST':
        if booking.car_returned == True:
            return HttpResponse(json.dumps({
                'type': 'S02',
                'msg': 'Car has been returned. Booking closed',
            }))
        else:
            booking.car_returned = True
            booking.fees_paid = True
            booking.save()
            supplier = booking.supplier
            phone = supplier.profile.phone
            send_sms_notification(str(phone), "go to 192.168.33.10:3000/book/{0}  to confirm car returned".format(booking.pk))
            return HttpResponse(json.dumps({
                'type': 'S01',
                'msg': 'Thank you',
            }))
