from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import Category, Product, Customer, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer
from .utils import send_order_notification


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=["get"])
    def average_price(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(category=category)
        avg_price = products.aggregate(Avg("price"))["price__avg"] or 0
        return Response({"average_price": avg_price})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_authenticated", False) and hasattr(user, "email"):
            return Order.objects.filter(customer__email=user.email)
        return Order.objects.none()

    def perform_create(self, serializer):
        order = serializer.save()
        send_order_notification(order)
