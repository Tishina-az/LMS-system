from rest_framework import generics, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson
from materials.paginators import CoursePaginator, LessonPaginator
from materials.serializers import CourseSerializer, LessonSerializer
from users.models import Subscribe
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Реализация CRUD для курса, с использованием Viewsets."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

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


class SubscribeAPIView(APIView):
    """API endpoint для управления подписками пользователя на курсы."""

    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("id")

        if not course_id:
            return Response({"error": "Введите корректный id курса."}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)
        subscribe = Subscribe.objects.filter(user=user, course=course)

        if subscribe.exists():
            subscribe.delete()
            message = "Подписка удалена"
        else:
            Subscribe.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)


class LessonListAPIView(generics.ListAPIView):
    """API endpoint для получения списка всех уроков."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    """API endpoint для создания нового урока."""

    serializer_class = LessonSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
