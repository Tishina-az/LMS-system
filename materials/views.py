from rest_framework import generics, viewsets

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    """Реализация CRUD для курса, с использованием Viewsets."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = [~IsModerator]
        else:
            self.permission_classes = [IsModerator]
        return super().get_permissions()


class LessonListAPIView(generics.ListAPIView):
    """API endpoint для получения списка всех уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]


class LessonCreateAPIView(generics.CreateAPIView):
    """API endpoint для создания нового урока."""

    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """API endpoint для получения деталей конкретного урока."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """API endpoint для обновления существующего урока."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """API endpoint для удаления урока."""

    queryset = Lesson.objects.all()
    permission_classes = [~IsModerator]
