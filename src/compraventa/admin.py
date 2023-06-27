from django.contrib import admin
from .models import Pedido, Producto, Proveedor, Cliente, Sucursal, Categoria


# Register your models here.
#admin.site.register(Pedido) deberían poder modificar los pedidos?
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(Cliente)
admin.site.register(Sucursal)
admin.site.register(Categoria)