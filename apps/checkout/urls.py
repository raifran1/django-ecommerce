from django.urls import path
from .views import CreateCartItemView, CartItemView, checkout_cart, order_list

urlpatterns = [
    path('carrinho/adicionar/<slug:slug>/', CreateCartItemView.as_view(), name='create_cartitem'),
    path('carrinho/', CartItemView.as_view(), name='cart'),
    path('finalizando/', checkout_cart, name='checkout'),
    path('pedidos/', order_list, name='pedidos'),
]