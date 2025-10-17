from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Почта")
    avatar = models.ImageField(upload_to="user/avatar", blank=True, null=True, verbose_name="Ава")
    phone_number = models.CharField(max_length=17, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=56, blank=True, null=True, verbose_name="Страна")
    is_verified = models.BooleanField(default=False, verbose_name="Подтвержден")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
