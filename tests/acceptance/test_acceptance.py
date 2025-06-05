"""
Acceptance test for the full order flow in the Products API service.
Covers customer, product, and order creation and retrieval via API.
"""

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Category, Product, Customer, Order
from unittest.mock import patch
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_acceptance_order_flow():
    client = APIClient()
    User = get_user_model()
    user = User.objects.create_user(
        username="bob", email="bob@example.com", password="testpass123"
    )
    customer = Customer.objects.create(
        first_name="Bob", last_name="Marley", email="bob@example.com"
    )
    # Create a category and product
    category = Category.objects.create(name="Music")
    product = Product.objects.create(name="Guitar", price=100, category=category)
    # Patch OIDC authentication and permission to always allow
    with (
        patch(
            "django_pyoidc.drf.authentication.OIDCBearerAuthentication.authenticate",
            return_value=(user, None),
        ),
        patch(
            "rest_framework.permissions.IsAuthenticated.has_permission",
            return_value=True,
        ),
    ):
        order_data = {
            "customer": customer.pk,
            "items": [{"product": product.pk, "quantity": 1}],
        }
        response = client.post(reverse("order-list"), order_data, format="json")
        assert response.status_code == 201
        order_uuid = response.data["uuid"]
        # Retrieve the order via API
        response = client.get(reverse("order-list"))
        assert response.status_code == 200
        data = response.data
        # Check if the created order exists in the response using its UUID
        order = next((o for o in data if o["uuid"] == order_uuid), None)
        assert order is not None
        assert order["customer"] == customer.pk
        assert order["items"][0]["product"] == product.pk
        assert order["items"][0]["quantity"] == 1
