from .models import Producto, Pedido, Proveedor, Categoria, Cliente
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        
class RegistrarUsuarioForm(UserCreationForm): # hereda del formulario usercreationform

    rut = forms.CharField(max_length=12)
    nombres = forms.CharField(max_length=30)
    apellidos = forms.CharField(max_length=30)
   
    telefono_movil = forms.CharField(max_length=30)
    telefono_fijo = forms.CharField(max_length=30)
 
    notas = forms.CharField(max_length=250)
    direcciones = forms.CharField(max_length=250)

  
    class Meta:
        model = User
  
        fields = UserCreationForm.Meta.fields + ('rut', 'nombres', 'apellidos', 'email', 'telefono_movil', 'telefono_fijo', 'notas', 'direcciones' )
