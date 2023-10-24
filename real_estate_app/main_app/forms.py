from django import forms
from django.core import validators
from . import models
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class SignUp(forms.Form):
    user = forms.CharField(label='User Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='PassWord')

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password1','password2','email')