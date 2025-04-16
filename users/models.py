from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона',
                                    help_text='Необязательное поле. Введите ваш номер телефона.')
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True, verbose_name='Аватар',
                               help_text='Загрузите изображение.')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
