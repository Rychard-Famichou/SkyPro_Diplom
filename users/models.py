from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


# Create your models here.
class CustomUserManager(BaseUserManager):
    def _generate_unique_username(self, first_name, last_name):
        base_username = slugify(f"{first_name}-{last_name}")
        if not base_username:
            base_username = "user"
        username = base_username
        counter = 1
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}-{counter}"
            counter += 1
        return username

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле Email обязательно для заполнения")
        if not first_name or not last_name:
            raise ValueError("Имя и Фамилия обязательны для заполнения")

        email = self.normalize_email(email)

        if not extra_fields.get("username"):
            extra_fields["username"] = self._generate_unique_username(first_name, last_name)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = "USER", "Пользователь"
        ADMIN = "ADMIN", "Администратор"

    username = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Никнейм")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Телефон")
    email = models.EmailField(max_length=50, unique=True, verbose_name="Почта")
    role = models.CharField(choices=RoleChoices.choices, verbose_name="Роль пользователя")
    image = models.ImageField(upload_to="avatars/%Y/%m", verbose_name="Аватарка")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.username and self.first_name and self.last_name:
            base = slugify(f"{self.first_name}-{self.last_name}")
            username = base
            counter = 1
            while CustomUser.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f"{base}-{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)
