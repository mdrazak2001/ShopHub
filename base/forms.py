from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm
from django.db import models
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_by', 'is_verified', 'created_at', 'is_sold']
