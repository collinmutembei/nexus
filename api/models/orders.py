import uuid
from django.db import models
from .customers import Customer
from .products import Product


class Order(models.Model):
    uuid = models.CharField(
        max_length=255, unique=True, default=uuid.uuid4, editable=False
    )
    customer = models.ForeignKey(
        Customer, related_name="orders", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"Order {self.uuid} - {self.customer}"

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.uuid})"

    class Meta:
        ordering = ["-order__created_at"]
