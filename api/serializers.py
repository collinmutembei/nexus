from rest_framework import serializers
from .models import Category, Product, Customer, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    uuid = serializers.UUIDField(read_only=True)
    status = serializers.CharField(read_only=True)
    total_amount = serializers.DecimalField(
        read_only=True, max_digits=10, decimal_places=2
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "uuid",
            "customer",
            "items",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Assuming Order model has a method or property to calculate total_amount
        representation["total_amount"] = str(instance.total_amount)
        return representation
