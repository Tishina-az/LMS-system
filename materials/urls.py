from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lesson/detail/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_detail"),
    path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lessons_update"),
    path("lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lessons_delete"),
]

urlpatterns += router.urls
