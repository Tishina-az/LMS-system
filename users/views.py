from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserCreateSerializer, UserDetailSerializer


class PaymentListAPIView(generics.ListAPIView):
    """API endpoint для получения списка всех платежей."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()


class UserViewSet(ViewSet):
    """Реализация CRUD для пользователя, с использованием Viewsets."""

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Выбор сериализатора (UserCreateSerializer или UserDetailSerializer),
         в зависимости от текущего действия (action)."""
        if self.action in ["create", "update", "partial_update"]:
            return UserCreateSerializer
        return UserDetailSerializer

    def create(self, request):
        """Создание пользователя."""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserDetailSerializer(user).data, status=201)

    def retrieve(self, request, pk=None):
        """Получение данных пользователя."""
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer_class()(user)
        return Response(serializer.data)
