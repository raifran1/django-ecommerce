from django.contrib import admin

# Register your models here.
from apps.checkout.models import Order

admin.site.register(Order)