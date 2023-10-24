from django import forms
from django.core import validators
from . import models
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .utils import get_foundation_categorie,get_neighborhood_categorie

class SignUp(forms.Form):
    user = forms.CharField(label='User Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='PassWord')

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password1','password2','email')



class RealEstateForm(forms.Form):
    # Numeric Features
    Year_Built = forms.IntegerField(label="Year Built")
    First_Flr_SF = forms.DecimalField(label="1st Flr SF")
    Gr_Liv_Area = forms.DecimalField(label="Gr Liv Area")
    Garage_Area = forms.DecimalField(label="Garage Area")
    Overall_Qual = forms.IntegerField(label="Overall Qual")
    Full_Bath = forms.IntegerField(label="Full Bath")

    # Ordinal Features
    Exter_Qual = forms.ChoiceField(
        label="Exterior Quality",
        choices=[('Ex', 'Excellent'), ('Gd', 'Good'), ('TA', 'Average'), ('Fa', 'Fair'), ('Po', 'Poor')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    Kitchen_Qual = forms.ChoiceField(
        label="Kitchen Quality",
        choices=[('Ex', 'Excellent'), ('Gd', 'Good'), ('TA', 'Average'), ('Fa', 'Fair'), ('Po', 'Poor')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Categorical Features
    Foundation = forms.ChoiceField(
        label="Foundation",
        choices=get_foundation_categorie(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Neighborhood = forms.ChoiceField(
        label="Neighborhood",
        choices=get_neighborhood_categorie(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )