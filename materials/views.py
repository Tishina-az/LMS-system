from rest_framework import viewsets, generics

from materials.models import Course
from materials.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Реализация CRUD для курса, с использованием Viewsets"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
