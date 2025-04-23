from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока."""

    class Meta:
        model = Lesson
        fields = "__all__"


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


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса с дополнительными полями."""

    lessons_count = SerializerMethodField()
    lessons = CourseLessonSerializer(many=True)

    def get_lessons_count(self, course):
        """Возвращает количество уроков в курсе."""
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "lessons_count",
            "lessons",
        )
        read_only_fields = ("id", "lessons_count", "lessons")
