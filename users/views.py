from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserCreateSerializer, UserDetailSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class PaymentListAPIView(generics.ListAPIView):
    """API endpoint для получения списка всех платежей."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ("date",)
    filterset_fields = (
        "paid_course",
        "paid_lesson",
        "method",
    )


class PaymentCreateAPIView(generics.CreateAPIView):
    """API endpoint для создания платежей."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.method == Payment.TRANSFER:
            # Для безналичной оплаты создаем stripe-сессию
            product = create_stripe_product(payment)
            price = create_stripe_price(payment.amount, product)
            session_id, link = create_stripe_session(price)
            payment.session_id = session_id
            payment.link = link
            payment.save()
        else:
            # Для наличной оплаты можно реализовать дополнительную логику
            pass


class UserViewSet(ViewSet):
    """Реализация CRUD для пользователя, с использованием Viewsets."""

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Выбор сериализатора (UserCreateSerializer или UserDetailSerializer),
        в зависимости от текущего действия (action)."""
        if self.action in ["create", "update", "partial_update", "register"]:
            return UserCreateSerializer
        return UserDetailSerializer

    @action(detail=False, methods=["post"], permission_classes=[AllowAny], authentication_classes=[])
    def register(self, request):
        """Создание (регистрация) пользователя."""
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserDetailSerializer(user).data, status=201)

    def retrieve(self, request, pk=None):
        """Получение данных пользователя."""
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer_class()(user)
        return Response(serializer.data)
