from django.contrib import admin
from .models import Product, Customer, Category, Order, OrderItem

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
