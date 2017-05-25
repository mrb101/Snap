from django.db import models

from django.contrib.auth.models import User

from .validators import validate_phone


class Profile(models.Model):
    """ TODO:
        Passport/IC Numer,
        Passport Number Valid Boolean,
        Licenese Number,
        Nationality,
        Company Name,
    """
    user = models.OneToOneField(User)
    phone = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        validators=[validate_phone]
    )
    supplier = models.BooleanField(default=False)
