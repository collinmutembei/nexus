import pytest
from api.models import Category, Product, Customer, Order, OrderItem

@pytest.mark.django_db
class TestCategoryModel:
    def test_str(self):
        category = Category.objects.create(name="Electronics")
        assert str(category) == "Electronics"

@pytest.mark.django_db
class TestProductModel:
    def test_str(self):
        category = Category.objects.create(name="Books")
        product = Product.objects.create(name="Django for APIs", price=10.0, category=category)
        assert str(product) == "Django for APIs"

@pytest.mark.django_db
class TestCustomerModel:
    def test_str(self):
        customer = Customer.objects.create(first_name="John", last_name="Doe", email="john@example.com")
        assert str(customer) == "John Doe"

@pytest.mark.django_db
class TestOrderModel:
    def test_total_amount(self):
        customer = Customer.objects.create(first_name="Jane", last_name="Smith", email="jane@example.com")
        category = Category.objects.create(name="Toys")
        product1 = Product.objects.create(name="Toy Car", price=5.0, category=category)
        product2 = Product.objects.create(name="Toy Train", price=15.0, category=category)
        order = Order.objects.create(customer=customer)
        OrderItem.objects.create(order=order, product=product1, quantity=2)
        OrderItem.objects.create(order=order, product=product2, quantity=1)
        assert order.total_amount == 25.0
