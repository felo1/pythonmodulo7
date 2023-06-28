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
        
class RegistrarUsuarioForm(UserCreationForm): # hereda del formulario
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField(max_length=64) #sólo se eligen algunos campos
  
    class Meta(UserCreationForm.Meta):
        model = User
  
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
