from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string


class User(AbstractUser):
    ROLE_USER = "user"
    ROLE_MANAGER = "manager"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_USER, "Пользователь"),
        (ROLE_MANAGER, "Менеджер"),
        (ROLE_ADMIN, "Администратор"),
    ]

    email = models.EmailField(unique=True, verbose_name="Почта")
    verification_token = models.CharField(max_length=12, blank=True, verbose_name="Ключ подтверждения")
    is_verified = models.BooleanField(default=False, verbose_name="Подтвержден")
    is_blocked = models.BooleanField(default=False, verbose_name="Заблокирован")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER, verbose_name="Роль")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    def generate_verification_token(self):
        token = get_random_string(12)
        self.verification_token = token
        self.save()
        return token

    @property
    def is_manager(self):
        return self.role == self.ROLE_MANAGER

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField(upload_to="user/avatar", blank=True, null=True, verbose_name="Ава")
    phone_number = models.CharField(max_length=17, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=56, blank=True, null=True, verbose_name="Страна")
    company = models.CharField(max_length=120, blank=True, null=True, verbose_name="Компания")

    def __str__(self):
        return f"Профиль {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
