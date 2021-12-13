from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm
from django.db import models
from .models import *


class DateTimeInput(forms.DateTimeInput):
    action_time = forms.DateTimeField()
