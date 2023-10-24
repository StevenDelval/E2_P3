from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Ajoutez des champs personnalisés ici

    class Meta:
        db_table = 'main_app_customuser'
        managed = True
