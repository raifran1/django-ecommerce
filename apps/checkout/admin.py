from django.contrib import admin

# Register your models here.
from apps.checkout.models import Order, CartItem, OrderItem

admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(OrderItem)