from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name="login"),
    path('lancamentos', views.lancamentos, name='lancamentos'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('perfil', views.perfil, name='perfil'),
]
