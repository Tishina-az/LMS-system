from rest_framework import generics

from users.models import Payment
from users.serializers import PaymentSerializer


class CourseListAPIView(generics.ListAPIView):
    """API endpoint для получения списка всех платежей."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
