from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import PasswordReset
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        
        
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
        
