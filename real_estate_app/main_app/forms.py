from django import forms
from django.core import validators
from . import models
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from .utils import get_foundation_categorie, get_neighborhood_categorie


class SignUp(forms.Form):
    user = forms.CharField(label='User Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='PassWord')


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2', 'email')


attrs = {
    'class': 'bg-gray-50 appearance-none border-black-gray '
    'text-gray-700 leading-tight focus:outline-none '
    'focus:border-bordeaux'
}


class RealEstateForm(forms.Form):
    # Caractéristiques numériques
    Year_Built = forms.IntegerField(
        label="Année de construction", min_value=1800, max_value=2023,
        widget=forms.NumberInput(attrs=attrs)
    )
    First_Flr_SF = forms.DecimalField(
        label="Superficie au 1er étage", min_value=0, max_value=95000,
        widget=forms.NumberInput(attrs=attrs)
    )
    Gr_Liv_Area = forms.DecimalField(
        label="Superficie habitable", min_value=0, max_value=910000,
        widget=forms.NumberInput(attrs=attrs)
    )
    Garage_Area = forms.DecimalField(
        label="Superficie du garage", min_value=0, max_value=93000,
        widget=forms.NumberInput(attrs=attrs)
    )
    Overall_Qual = forms.IntegerField(
        label="Qualité générale", min_value=0, max_value=10,
        widget=forms.NumberInput(attrs=attrs)
    )
    Full_Bath = forms.IntegerField(
        label="Salles de bains complètes", min_value=0, max_value=100,
        widget=forms.NumberInput(attrs=attrs)
    )

    # Caractéristiques ordinales
    Exter_Qual = forms.ChoiceField(
        label="Qualité de l'extérieur",
        choices=[('Ex', 'Excellent'), ('Gd', 'Bon'),
                 ('TA', 'Moyen'), ('Fa', 'Mauvais'), ('Po', 'Très mauvais')],
        widget=forms.Select(attrs=attrs)
    )

    Kitchen_Qual = forms.ChoiceField(
        label="Qualité de la cuisine",
        choices=[('Ex', 'Excellent'), ('Gd', 'Bon'),
                 ('TA', 'Moyen'), ('Fa', 'Mauvais'), ('Po', 'Très mauvais')],
        widget=forms.Select(attrs=attrs)
    )

    # Caractéristiques catégorielles
    Foundation = forms.ChoiceField(
        label="Fondation",
        choices=get_foundation_categorie(),
        widget=forms.Select(attrs=attrs)
    )
    Neighborhood = forms.ChoiceField(
        label="Quartier",
        choices=get_neighborhood_categorie(),
        widget=forms.Select(attrs=attrs)
    )
