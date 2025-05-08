import stripe
from rest_framework.reverse import reverse

from config import settings

stripe.api_key = settings.STRIPE_API_KEY

def create_stripe_product(payment):
    """Создает продукт в stripe для оплаты."""

    name = payment.paid_course.title if payment.paid_course else payment.paid_lesson.title
    product = stripe.Product.create(name=name)
    return product.id


def create_stripe_price(amount, product):
    """Создает цену в stripe."""

    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(float(amount) * 100),
        product_data={"name": product},
    )
    return price


def create_stripe_session(price, payment_id):
    """Создает сессию в stripe для оплаты."""

    session = stripe.checkout.Session.create(
        success_url=f"http://127.0.0.1:8000/{reverse("users:payment_status", kwargs={'id': payment_id})}",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def get_retrieve_stripe_session(session_id):
    """Получает статус(детализацию) платежа в stripe-сессии."""

    session = stripe.checkout.Session.retrieve(session_id)
    return {
        "status": session.status,
        "payment_status": session.payment_status,
        "amount_total": session.amount_total / 100,
        "currency": session.currency,
    }
