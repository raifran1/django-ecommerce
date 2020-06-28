from django.urls import path
from .views import product_detail, products, category_detail

urlpatterns = [
    path('produtos/', products, name='products'),
    path('produto/<slug:slug>', product_detail, name='product_detail'),
    path('categoria/<int:id>', category_detail, name='category_detail'),
]