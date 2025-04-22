from django.urls import path

from users.apps import UsersConfig
from users.views import CourseListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", CourseListAPIView.as_view(), name="payments_list"),
]
