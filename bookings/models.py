from django.db import models

import uuid
from datetime import timedelta

from django.contrib.auth.models import User
from cars.models import Car, Category

class Booking(models.Model):
    HALF_DAY = timedelta(hours=6)
    DAY = timedelta(days=1)
    WEEK = timedelta(days=7)
    MONTH = timedelta(weeks=4)
    DURATION = (
        (HALF_DAY, 'Six Hours'),
        (DAY, 'One Day'),
        (WEEK, 'One Week'),
        (MONTH, 'One Month'),
    )
    booking_number = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    customer = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    starts = models.DateTimeField(null=True)
    duration = models.DurationField(
        max_length=2,
        choices=DURATION,
        default=DAY,
    )
    dropoff = models.CharField(max_length=255, null=False, blank=False)
    booking_confirmed = models.BooleanField(default=False)
    car = models.ForeignKey(Car, null=True, blank=True)
    car_deliverd = models.BooleanField(default=False)
    car_returned = models.BooleanField(default=False)
    fees_paid = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.booking_number)

    def __str__(self):
        return str(self.booking_number)

    def __repr__(self):
        return str(self.booking_number)

    @property
    def rental_ends(self):
        ends = self.starts + self.duration
        return ends

    def is_confirmed(self):
        if self.booking_confirmed:
            return True
        return False

    def is_deliverd(self):
        if self.car_deliverd:
            return True
        return False

    def is_returned(self):
        if self.car_returned:
            return True
        return False

    def is_paid(self):
        if self.fees_paid:
            return True
        return False
