from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("payments/", PaymentListAPIView.as_view(), name="payments_list"),

    # Получение JWT-токенов, для авторизации и аутентификации
    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
]

urlpatterns += router.urls
