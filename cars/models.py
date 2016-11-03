from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
    ECO = 'ECO'
    SED = 'SED'
    FAM = 'FAM'
    CAR_CONCEPT = (
        (ECO, 'Economy'),
        (SED, 'Sedan'),
        (FAM, 'Family')
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    concept = models.CharField(
        help_text="Choose the car the type",
        max_length=255,
        blank=False,
        null=False,
        choices=CAR_CONCEPT
    )

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Car(models.Model):
    category = models.ForeignKey(Category)
    gps_number = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=False, null=False)
    model = models.CharField(max_length=100, blank=False, null=False)
    year = models.DateTimeField()
    plate_number = models.CharField(max_length=10, blank=False, null=False)
    road_tax_validation = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __unicode__(self):
        return "{0} - {1}".format(self.model, self.plate_number)

    def __str__(self):
        return "{0} - {1}".format(self.model, self.plate_number)

    def __repr__(self):
        return "{0} - {1}".format(self.model, self.plate_number)


