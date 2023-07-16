"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from . import views 

urlpatterns = [
    path("", views.ClientePedidoListView.as_view(), name = "index"),
    path("registro", views.registrar_usuario, name='registro'),
    path("login", views.login_view, name='login'),
    path("login/", RedirectView.as_view(pattern_name='login', permanent=True)),
    #path("hola", views.hola, name="hola"),
    path("logout", views.logout_view, name="logout"),
    path("agregar_al_carro", views.ProductoListView.as_view(), name="productos"),
    path("pedido_list_gestion", views.GestiónPedidoListView.as_view(), name="gestion-pedidos"),
    #cambie el login welcome para que muestre los pedidos.
    #quiero que el home sea esta vista tb cuando estás logeado pero no staff. si es staff, que envie
    #a admin
    path("pedido_list_cliente", views.ClientePedidoListView.as_view(), name="hola"),
    #path("tomar_pedido", views.buscar_usuario, name="tomar-pedido"),
    #cambié esto para que también restringa el acceso a tomar pedidos
    path("tomar_pedido", views.TomarPedidoListView.as_view(), name="tomar-pedido"),
    path("tomar_pedido_paso2", views.tomar_pedido_paso2, name="tomar_pedido_paso2"),
    path("tomar_pedido_paso3", views.Tomar_pedido_paso3.as_view(), name="tomar_pedido_paso3"),
    path('pedidos/<str:pk>/edit/', views.PedidoEditView.as_view(), name='edit_pedido'),
]
   # path("pedido_manual", views.pedido_manual, name = "pedido_manual"),
   # path("pedido_manual_cliente", views.pedido_manual_cliente, name = "pedido_manual_cliente"),