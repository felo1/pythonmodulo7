from .models import Producto, Pedido, Categoria, Cliente, ItemPedido
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import modelform_factory

PedidoForm = modelform_factory(Pedido, fields=['cliente_solicitante', 'estado_despacho', 'direccion_despacho']) #tiene_despacho tira error

DetallePedidoForm = modelform_factory(Pedido, fields=['estado_despacho','direccion_despacho'])

ItemPedidoForm = modelform_factory(ItemPedido, fields=['producto', 'cantidad'])

class ingreso_clientes(forms.ModelForm):
   class Meta:
        model = Cliente
        fields = '__all__' 
        
class RegistrarUsuarioForm(UserCreationForm): # hereda del formulario usercreationform

    rut = forms.CharField(max_length=12)
    nombres = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=30)
    telefono_movil = forms.CharField(max_length=30)
    telefono_fijo = forms.CharField(max_length=30)
    notas = forms.CharField(max_length=250)
  
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('rut', 'nombres', 'apellidos', 'email', 'telefono_movil', 'telefono_fijo', 'notas')
"""


class pedidos_manuales(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'cliente_solicitante', 
            'productos',
            ]
        
class pedidos_manuales_cliente(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'productos',
            ]        

"""