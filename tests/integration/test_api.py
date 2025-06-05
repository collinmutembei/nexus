"""
Integration tests for API endpoints in the Products API service.
Covers category, product, and order API flows.
"""

import pytest
from rest_framework.test import APIClient
from api.models import Category, Product, Customer
from django.urls import reverse
from unittest.mock import patch


@pytest.mark.django_db
def test_category_list():
    client = APIClient()
    parent = Category.objects.create(name="Electronics")
    Category.objects.create(name="Phones", parent=parent)
    with patch(
        "rest_framework.permissions.IsAuthenticated.has_permission", return_value=True
    ):
        response = client.get(reverse("category-list"))
    assert response.status_code == 200
    assert response.data[0]["name"] == "Phones"


@pytest.mark.django_db
def test_category_create_with_parent():
    client = APIClient()
    parent = Category.objects.create(name="Electronics")
    data = {"name": "Smartphones", "parent": parent.pk}
    with patch(
        "rest_framework.permissions.IsAuthenticated.has_permission", return_value=True
    ):
        response = client.post(reverse("category-list"), data)
    assert response.status_code == 201
    assert response.data["name"] == "Smartphones"
    assert response.data["parent"] == parent.pk


@pytest.mark.django_db
def test_product_create():
    client = APIClient()
    category = Category.objects.create(name="Laptops")
    data = {"name": "MacBook", "price": 1000, "category": category.pk}
    with patch(
        "rest_framework.permissions.IsAuthenticated.has_permission", return_value=True
    ):
        response = client.post(reverse("product-list"), data)
    assert response.status_code == 201
    assert response.data["name"] == "MacBook"


@pytest.mark.django_db
def test_order_create():
    client = APIClient()
    customer = Customer.objects.create(
        first_name="Alice", last_name="Smith", email="alice@example.com"
    )
    category = Category.objects.create(name="Games")
    product = Product.objects.create(name="Chess", price=20, category=category)
    data = {"customer": customer.pk, "items": [{"product": product.pk, "quantity": 2}]}
    with (
        patch(
            "django_pyoidc.drf.authentication.OIDCBearerAuthentication.authenticate",
            return_value=(customer, None),
        ),
        patch(
            "rest_framework.permissions.IsAuthenticated.has_permission",
            return_value=True,
        ),
    ):
        response = client.post(reverse("order-list"), data, format="json")
    assert response.status_code == 201
    assert response.data["customer"] == customer.pk


@pytest.mark.django_db
def test_category_average_price_with_products():
    client = APIClient()
    parent = Category.objects.create(name="Electronics")
    category = Category.objects.create(name="Smartphones", parent=parent)
    Product.objects.create(name="iPhone", price=1000, category=category)
    Product.objects.create(name="Android", price=500, category=category)
    with patch("rest_framework.permissions.IsAuthenticated.has_permission", return_value=True):
        response = client.get(reverse("category-average-price", args=[category.pk]))
    assert response.status_code == 200
    assert response.data["average_price"] == 750


@pytest.mark.django_db
def test_category_average_price_no_products():
    client = APIClient()
    category = Category.objects.create(name="EmptyCat")
    with patch("rest_framework.permissions.IsAuthenticated.has_permission", return_value=True):
        response = client.get(reverse("category-average-price", args=[category.pk]))
    assert response.status_code == 200
    assert response.data["average_price"] == 0
