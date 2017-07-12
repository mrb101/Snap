from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth.models import User

import nexmo
from app.settings import API_KEY, API_SEC
from cars.models import Category

from .models import Booking
from .forms import (
    BookingForm,
    BookingConfirmationForm,
    CarDeliveryForm,
    BookingClosingForm,
)


class CreateBooking(View):
    template_name = "bookings/form.html"

    def get(self, request, *args, **kwargs):
        context = {}
        if not request.user.profile.supplier:
            form = BookingForm()
            context['form'] = form
            return render(request, self.template_name, context)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        context = {}
        if not request.user.profile.supplier:
            form = BookingForm(request.POST)
            start = request.POST.get('starts')
            duration = request.POST.get('duration')
            address = request.POST.get('dropoff')
            category = Category.objects.get(pk=request.POST.get('category'))
            starts = start
            booking_data = ({
                'category': request.POST.get('category'),
                'starts': starts,
                'dropoff': address,
                'duration': duration
            })
            booking_form = BookingForm(booking_data)
            if booking_form.is_valid():
                booking_object = booking_form.save(commit=False)
                booking_object.customer = request.user
                booking_object.save()
                suppliers = User.objects.filter(profile__supplier=True)
                client = nexmo.Client(key=API_KEY, secret=API_SEC)
                for supplier in suppliers:
                    response = client.send_message({
                        'from': 'Cruz',
                        'to': supplier.profile.phone,
                        'text': "New Booking at cruz.ninja/booking/{}/".format(booking_object.booking_number)
                    })
                    response_message = response['messages'][0]
                    if response_message['status'] == '0':
                        print("message sent")
                    else:
                        print("message not sent")
                messages.success(
                request,
                'Your booking request has been submitted. Please wait for confirmation'
            )
                return redirect("/")
            else:
                context['form'] = booking_form
                messages.error(
                    request,
                    'Some fields has errors. please recheck.'
                )
                return render(request, self.template_name, context)
        else:
            messages.error(
                request,
                'Suppliers can not book cars.'
            )
            return redirect("/")


class BookingDetails(View):

    def get_booking(self):
        return Booking.objects.get(booking_number=self.kwargs['booking_number'])

    def get(self, request, *args, **kwargs):
        booking = self.get_booking()
        if not booking.booking_confirmed:
            return redirect("booking:confirm_booking", booking_number=booking.booking_number)
        elif not booking.car_deliverd:
            return redirect("booking:car_delivered", booking_number=booking.booking_number)
        elif not booking.car_returned:
            return redirect("booking:car_return", booking_number=booking.booking_number)
        elif not booking.fees_paid:
            return redirect("booking:booking_fees", booking_number=booking.booking_number)
        else:
            return redirect("booking:booking_closed", booking_number=booking.booking_number)



class ConfirmBooking(View):
    template_name = "bookings/booking_details.html"

    def get_booking(self):
        return Booking.objects.get(booking_number=self.kwargs['booking_number'])

    def get(self, request, *args, **kwargs):
        context = {'booking': self.get_booking()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.user.profile.supplier:
            context = {}
            booking = self.get_booking()
            booking.booking_confirmed = True
            booking.supplier = request.user
            booking.save()
            client = nexmo.Client(key=API_KEY, secret=API_SEC)
            response = client.send_message({
                'from': "Cruz",
                'to': booking.customer.profile.phone,
                'text': 'Your booking has been confirmed. go to curz.ninja/booking/{}/'.format(bookgin.booking_number),
            })
            response_message = response['messages'][0]
            if response_message['status'] == '0':
                print("message sent")
            else:
                print("message not sent")
            messages.success(
                request,
                'You have confirmed the booking.'
            )
            return redirect("/")
        else:
            messages.error(
                request,
                "You can't confirm this booking."
            )
            return render(request, self.template_name, context)


class BookingDelivered(View):
    template_name = "bookings/car_delivered.html"

    def get_booking(self):
        return Booking.objects.get(booking_number=self.kwargs['booking_number'])

    def get(self, request, *args, **kwargs):
        context = {'booking': self.get_booking()}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.user.profile.supplier:
            context = {}
            booking = self.get_booking()
            booking.car_deliverd = True
            booking.save()
            client = nexmo.Client(key=API_KEY, secret=API_SEC)
            response = client.send_message({
                'from': "Cruz",
                'to': booking.customer.profile.phone,
                'text': 'Your car is here'
            })
            response_message = response['messages'][0]
            if response_message['status'] == '0':
                print("message sent")
            else:
                print("message not sent")
            messages.success(
                request,
                'Message has been sent'
            )
            return redirect("/")
        else:
            messages.error(
                request,
                "Something is wrong."
            )
            return render(request, self.template_name, context)


class BookingReturn(View):
    template_name = "bookings/car_return.html"

    def get_booking(self):
        return Booking.objects.get(booking_number=self.kwargs['booking_number'])

    def get(self, request, *args, **kwargs):
        if not request.user.profile.supplier:
            context = {'booking': self.get_booking}
            return render(request, self.template_name, context)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        if not request.user.profile.supplier:
            booking = self.get_booking()
            booking.car_returned = True
            booking.save()
            client = nexmo.Client(key=API_KEY, secret=API_SEC)
            response = client.send_message({
                'from': "Cruz",
                'to': booking.customer.profile.phone,
                'text': 'Car has be returned. cruz.ninja/booking/{}/'.format(booking.booking_number)
            })
            response_message = response['messages'][0]
            if response_message['status'] == '0':
                print("message sent")
            else:
                print("message not sent")
            messages.success(
                request,
                'The Supplier is being notified.'
            )
            return redirect("/")
        else:
            context = {}
            messages.error(
                request,
                "something wrong happned. Please try again."
            )
            return render(request, self.template_name, context)


class BookingFees(View):
    template_name = "bookings/fees_paid.html"

    def get_booking(self):
        return Booking.objects.get(booking_number=self.kwargs['booking_number'])

    def get(self, request, *args, **kwargs):
        if request.user.profile.supplier:
            context = {'booking': self.get_booking()}
            return render(request, self.template_name, context)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        if request.user.profile.supplier:
            booking = self.get_booking()
            booking.fees_paid = True
            booking.save()
            messages.success(
                request,
                'the booking is closed'
            )
            return redirect("/")
        else:
            messages.error(
                request,
                "something went wrong. Please try again."
            )
            return render(request, self.template_name, context)


class BookingClosed(View):
    template_name = "bookings/closed_booking.html"

    def get_booking(self):
        return Booking.objects.get(booking_number=self.kwargs['booking_number'])

    def get(self, request, *args, **kwargs):
        if request.user.profile.supplier:
            context = {'booking': self.get_booking()}
            return render(request, self.template_name, context)
        else:
            return redirect("/")

    def post(self, request, *args, **kwargs):
        pass
