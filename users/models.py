from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, verbose_name="телефон", null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name="город", null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", verbose_name="аватарка", null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
