from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


class CustomUser(AbstractUser):
    # Ajoutez des champs personnalisés ici

    class Meta:
        db_table = 'main_app_customuser'
        managed = True


class RealEstate(models.Model):
    # Caractéristiques numériques
    Year_Built = models.IntegerField(
        verbose_name="Année de construction",
        validators=[MinValueValidator(1800), MaxValueValidator(2023)]
    )
    First_Flr_SF = models.DecimalField(
        verbose_name="Superficie au 1er étage",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(95000)]
    )
    Gr_Liv_Area = models.DecimalField(
        verbose_name="Superficie habitable",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(910000)]
    )
    Garage_Area = models.DecimalField(
        verbose_name="Superficie du garage",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(93000)]
    )
    Overall_Qual = models.IntegerField(
        verbose_name="Qualité générale",
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    Full_Bath = models.IntegerField(
        verbose_name="Salles de bains complètes",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    # Caractéristiques ordinales
    Exter_Qual = models.CharField(
        verbose_name="Qualité de l'extérieur",
        max_length=2,
        choices=[('Ex', 'Excellent'), ('Gd', 'Bon'),
                 ('TA', 'Moyen'), ('Fa', 'Mauvais'), ('Po', 'Très mauvais')]
    )

    Kitchen_Qual = models.CharField(
        verbose_name="Qualité de la cuisine",
        max_length=2,
        choices=[('Ex', 'Excellent'), ('Gd', 'Bon'),
                 ('TA', 'Moyen'), ('Fa', 'Mauvais'), ('Po', 'Très mauvais')]
    )

    # Caractéristiques catégorielles
    Foundation = models.CharField(
        verbose_name="Fondation",
        max_length=255
    )

    Neighborhood = models.CharField(
        verbose_name="Quartier",
        max_length=255
    )
    User = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Created_at = models.DateTimeField(auto_now_add=True)
    Pred = models.DecimalField(
        verbose_name="prix predit",
        max_digits=100,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100000000000)]
    )
