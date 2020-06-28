from django.urls import path
from .views import index, contact
from haystack.views import SearchView

urlpatterns = [
    path('', index, name='index'),
    path('contato/', contact, name='contact'),
    path('busca/', SearchView(), name='haystack_search'),
]