from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """Модель пользователя."""

    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Необязательное поле. Введите ваш номер телефона.",
    )
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(
        upload_to="avatar/", blank=True, null=True, verbose_name="Аватар", help_text="Загрузите изображение."
    )

    def __str__(self):
        return self.email

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Модель платежа."""

    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHOD = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="payments", verbose_name="Пользователь"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата платежа")
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Оплаченный урок",
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Сумма оплаты")
    method = models.CharField(max_length=8, choices=PAYMENT_METHOD, default=TRANSFER, verbose_name="Способ оплаты")
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="Id сессии")
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name="Ссылка на оплату")

    def __str__(self):
        return f"{self.user} - {self.paid_course if self.paid_course else self.paid_lesson} - {self.amount}."

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ["-date"]


class Subscribe(models.Model):
    """Модель подписки на обновления курса для пользователя."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribes", verbose_name="Пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscribes", verbose_name="Курс")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    def __str__(self):
        return f"Пользователь {self.user} подписан на {self.course}."

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = (
            "user",
            "course",
        )
