from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Для детального отображения платежей (с user)."""

    class Meta:
        model = Payment
        fields = "__all__"


class PaymentNestedSerializer(serializers.ModelSerializer):
    """Для вложенного отображения в User (без user)."""

    class Meta:
        model = Payment
        exclude = ("user",)


class UserCreateSerializer(serializers.ModelSerializer):
    """Для создания и редактирования пользователя."""

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
        )
        extra_kwargs = {"password": {"write_only": True}}


class UserDetailSerializer(serializers.ModelSerializer):
    """Для детального просмотра пользователя без критичных полей (типа пароль, статус пользователя и т.п.)."""

    payments = PaymentNestedSerializer(many=True, help_text="История платежей пользователя")

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
            "payments",
        )
