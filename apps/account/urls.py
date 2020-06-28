from django.urls import path
from .views import user_login, user_logout, account, add_user, change_password

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('minha-conta/', account, name='account'),
    path('novo-usuario/', add_user, name='add_user'),
    path('alterar-senha/', change_password, name='change_password'),
]