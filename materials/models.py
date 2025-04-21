from django.db import models

# from users.models import User


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="preview/", blank=True, null=True, verbose_name="Превью", help_text="Загрузите изображение"
    )
    description = models.TextField(verbose_name="Описание")

    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses", verbose_name="Владелец")

    def __str__(self):
        return f"Курс: {self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(max_length=100, verbose_name="Название урока")
    preview = models.ImageField(
        upload_to="preview/", blank=True, null=True, verbose_name="Превью", help_text="Загрузите изображение"
    )
    description = models.TextField(verbose_name="Описание")
    link = models.URLField(
        verbose_name="Ссылка на видео",
        blank=True,
        null=True,
        help_text="Укажите ссылку на видео (RuTube, YouTube и т.д.)",
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")

    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons", verbose_name="Владелец")

    def __str__(self):
        return f"Урок: {self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]
