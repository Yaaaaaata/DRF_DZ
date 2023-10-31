from django.db import models

from django.contrib.auth.models import AbstractUser
from classes.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    city = models.CharField(max_length=100, verbose_name="город", **NULLABLE)
    avatar = models.ImageField(upload_to="avatars/", verbose_name="аватарка", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
