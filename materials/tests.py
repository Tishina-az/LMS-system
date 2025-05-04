from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User, Subscribe


class MaterialsTestCase(APITestCase):
    """Тесты проверяют корректность работы CRUD уроков и подписки"""

    def setUp(self):
        self.user = User.objects.create(email="example@example.com")
        self.course = Course.objects.create(title="Введение в программирование", description="Описание курса", owner=self.user)
        self.lesson = Lesson.objects.create(title="Первый урок", description="Описание урока", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "title": "Второй урок",
            "description": "Описание второго урока",
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "title": "Третий урок"
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), "Третий урок"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_subscribe_create(self):
        url = reverse("materials:subscribes")
        data = {"id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data.get("message"), "Подписка добавлена"
        )
        self.assertEqual(
            Subscribe.objects.all().count(), 1
        )

    def test_subscribe_delete(self):
        Subscribe.objects.create(user=self.user, course=self.course)
        url = reverse("materials:subscribes")
        data = {"id": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data.get("message"), "Подписка удалена"
        )
        self.assertEqual(
            Subscribe.objects.all().count(), 0
        )
