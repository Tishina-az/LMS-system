from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Реализация CRUD для курса, с использованием Viewsets."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        elif self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonListAPIView(generics.ListAPIView):
    """API endpoint для получения списка всех уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """API endpoint для создания нового урока."""

    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """API endpoint для получения деталей конкретного урока."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner, IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """API endpoint для обновления существующего урока."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner, IsAuthenticated]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """API endpoint для удаления урока."""

    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]
