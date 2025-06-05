"""
Unit tests for utility functions in the Products API service.
Covers notification logic and external service integration.
"""

import pytest
from api.utils import send_order_notification
from api.models import Customer, Order, Product, Category, OrderItem
from unittest.mock import patch, MagicMock


@pytest.mark.django_db
def test_send_order_notification_sends_email_and_sms():
    customer = Customer.objects.create(
        first_name="Test",
        last_name="User",
        email="test@example.com",
        phone="+1234567890",
    )
    category = Category.objects.create(name="TestCat")
    product = Product.objects.create(name="TestProd", price=10, category=category)
    order = Order.objects.create(customer=customer)
    OrderItem.objects.create(order=order, product=product, quantity=1)
    with (
        patch("api.utils.send_mail") as mock_send_mail,
        patch("api.utils.africastalking") as mock_africastalking,
    ):
        mock_sms = MagicMock()
        mock_africastalking.SMS = mock_sms
        send_order_notification(order)
        mock_send_mail.assert_called_once()
        mock_africastalking.initialize.assert_called_once()
        mock_sms.send.assert_called_once()
