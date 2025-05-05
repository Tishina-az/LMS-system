from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import LinkValidator
from users.models import Subscribe


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока."""

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ("owner",)
        validators = [LinkValidator(field="link")]


class CourseLessonSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор урока для вложенного отображения в курсе."""

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "description",
            "link",
        )
        read_only_fields = ("id",)
        validators = [LinkValidator(field="link")]


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор подписки на курс."""

    class Mets:
        model = Subscribe
        fields = "__all__"
        read_only_fields = (
            "user",
            "created_at",
        )


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса с дополнительными полями."""

    lessons_count = SerializerMethodField()
    lessons = CourseLessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "owner",
            "lessons_count",
            "lessons",
            "is_subscribed",
        )
        read_only_fields = ("id", "owner", "lessons_count", "lessons")

    def get_lessons_count(self, course):
        """Возвращает количество уроков в курсе."""
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, obj):
        """Возвращает статус подписки текущего пользователя на данный курс"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(user=request.user, course=obj).exists()
        return False
