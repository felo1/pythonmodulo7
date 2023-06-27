from .models import Producto, Pedido, Proveedor, Categoria, Cliente
from django import forms

class ingreso_clientes(forms.ModelForm):
   class Meta:
        model = Cliente
        fields = '__all__' 

class pedidos_manuales(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'cliente_solicitante', 
            'productos',
            ]
