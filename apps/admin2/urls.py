from django.urls import path
from .views import product_create_admin, product_detail_admin, product_edit_admin, product_list_admin, index_admin, \
    category_create, categories, product_delete_admin, category_delete, category_edit
from haystack.views import SearchView


urlpatterns = [
    path('', index_admin, name='index_admin'),
    path('produtos/', product_list_admin, name='product_list_admin'),
    path('novo-produto/', product_create_admin, name='product_create_admin'),
    path('produto/<slug:slug>', product_detail_admin, name='product_detail_admin'),
    path('editar-produto/<slug:slug>', product_edit_admin, name='product_edit_admin'),
    path('apagar-produto/<slug:slug>', product_delete_admin, name='product_delete_admin'),

    path('apagar-categoria/<int:id>', category_delete, name='category_delete'),
    path('editar-categoria/<int:id>', category_edit, name='category_edit'),
    path('nova-categoria/', category_create, name='category_create'),
    path('categorias/', categories, name='categories'),

    path('busca/', SearchView(template='admin2/search.html'), name='haystack_search_admin'),
]