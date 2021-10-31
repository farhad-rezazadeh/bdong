from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    wallet = models.DecimalField(default=0.00, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
