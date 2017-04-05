from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .validators import validate_phone

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(max_length=30, validators=validate_phone)


    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
