
from django.utils import timezone
from django.views.generic.list import ListView
from django.shortcuts import render
from .models import Categoria, Cliente, Pedido, Producto, ItemPedido
from .forms import RegistrarUsuarioForm, PedidoForm, ItemPedidoForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
#from .forms import pedidos_manuales, pedidos_manuales_cliente
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
# Create your views here.
#
def index(request):
    return render(request, 'compraventa/index.html')



def login_view(request): #el form está directo en el template login.html
    if 'next' in request.GET:
        #si en la url está la palabra "next", generada al redirigir desde @login_required, enviar mensaje.
        messages.add_message(request, messages.INFO, 'Debe ingresar para acceder a las funcionalidades.')

    if request.method == "POST":
        username = request.POST["usuario"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            
            login(request, user)
            return HttpResponseRedirect(reverse("hola"))
        else:
            context= ["Credenciales Inválidas"]#si no lo hago como lista, itera por cada caracter del string.
            return render(request, "compraventa/login.html", {"messages": context})

    return render(request, "compraventa/login.html") #view del login

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        print(form)
        if form.is_valid():
            
            user = form.save() #guardar formulario
            grupo = Group.objects.get(name='usuario_cliente') #buscar el grupo
            user.groups.add(grupo)  #asignarlo al usuario
            cliente = Cliente(
                user=user,
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                rut=form.cleaned_data['rut'],
                telefono_movil=form.cleaned_data['telefono_movil'],
                telefono_fijo=form.cleaned_data['telefono_fijo'],
                notas= form.cleaned_data['notas'],
                #direcciones=form.cleaned_data['direcciones']
            )
            cliente.save()
            messages.success(request, 'Usuario ingresado exitosamente')
            return redirect('login')
    else:
        form = RegistrarUsuarioForm()
        
    return render(request, "compraventa/registro.html", {'form': form})
def hola(request):
    return render(request,"compraventa/hola.html")

def logout_view(request):
    
    logout(request)
    return render(request, "compraventa/logout.html")



class ProductoListView(ListView,LoginRequiredMixin):
    model = Producto
    paginate_by = 10  # if pagination is desired
    

    def get_context_data(self, **kwargs): #override del método de la clase padre, que es un generador de contexto para pasarlo al template
        context = super().get_context_data(**kwargs) #llama al método de la clase padre ListView usando super()
        pedido_form = PedidoForm() #se instancia un formulario PedidoForm vacío
        itempedido_form = ItemPedidoForm() #formulario vacío
        context['pedido_form'] = pedido_form #se agrega pedido_form a la lista de contextos
        context['itempedido_form'] = itempedido_form #y el otro form
        return context #contexto final   
    
    def post(self, request, *args, **kwargs): #override de post de la clase padre (ListView)
        #id_producto = request.POST.get('id_producto') #obtiene el tarea_ide de los parámetros del POST, cada vez que se presiona "Completar" o "Eliminar"
        #producto = Producto.objects.get(id_producto=id_producto) #obtiene el objeto Tarea asociado al tarea_id obtenido en la línea anterior.
        #item_pedido = ItemPedido.objects.get(id=id_producto)
        

        user_id = request.user.id #id de usuario logueado
       
        cliente_id = Cliente.objects.get(user_id=user_id) #obtiene el cliente a partir del usuario, recordar que cliente tiene
        #relación 1 a 1 con un usuario.
       
        pedido = Pedido.objects.create(cliente_solicitante=cliente_id) #TODO: encontrar la forma de que se mantenga el nro de pedido
        #y no se genere un nuevo pedido cada vez que se genera un item_pedido
       
        if 'cantidad' in request.POST: #si en el POST viene un campo 'cantidad':
            #cliente_actual = self.user.cliente
            #pedido = Pedido.objects.create() #algo asi, ccreo que falta asignar en este punto el cliente
            pedido.save()#guarda
            cantidad = request.POST['cantidad'] #actualiza el campo con el valor correspondiente
            id_producto = request.POST['id_producto']
            producto = Producto.objects.get(id_producto=id_producto) #obtiene INSTANCIA del producto en cuestión
            item_pedido = ItemPedido.objects.create(cantidad=cantidad, pedido=pedido, producto=producto) #instancia item_pedido
   
            item_pedido.save()    
    
        item_pedido.save() #guarda
        return redirect('productos') #redirige al listview, reflejándose el cambio de inmediato.
 









"""

class TareasListView(ListView): #listview es un class-based-view de django, que da la funcionalidad para mostrar datos en formato de lista.
    #los parámetros se asignan a variables
    model = Tarea #se indica modelo
    template_name = "gestor_app/listview_tareas.html" #nombre del template
    ordering = ['vencimiento_fecha', 'vencimiento_hora'] #orden, se dan dos keys, porque la fecha y hora en mi modelo son dos variables separadas

    def get_context_data(self, **kwargs): #override del método de la clase padre, que es un generador de contexto para pasarlo al template
        context = super().get_context_data(**kwargs) #llama al método de la clase padre ListView usando super()
        tarea_form = TareaForm() #se instancia un formulario TareaForm vacío
        context['tarea_form'] = tarea_form #se agrega el tarea_form al dict de contexto 
        
        return context #contexto final

    def get_queryset(self): #override del método de la clase padre para obtener los queryset que necesitemos para dar la funcionalidad de filtrado
        queryset = super().get_queryset() #super() a la clase padre, para obtener el queryset inicial
    
        estado_filter = self.request.GET.get('estado_filter') #si se ha seleccionado un filtro de estado, se asigna a esta variable
        categoria_filter = self.request.GET.get('categoria_filter') #si se ha seleccionado un filtro de categoría, se asigna a esta variable
        #estas variables no se asignan si el usuario no selecciona filtros

        user = self.request.user #se asigna el usuario logueado a una variable para usarlo más abajo.

        #si se cumplen las siguientes pruebas lógicas, se realiza un queryset con los parámetros indicados por los choicefields:

        if estado_filter and categoria_filter: # si el usuario ha filtrado por estado Y categoría            
            queryset = queryset.filter(estado=estado_filter, categoría=categoria_filter, usuario=user)
             
        elif estado_filter: # si el usuario ha filtrado sólo por estado,
            # Filtering by estado only
            queryset = queryset.filter(estado=estado_filter, usuario=user)
        elif categoria_filter: # si el usuario ha filtrado sólo por categoría,
            # Filtering by categoria only
            queryset = queryset.filter(categoría=categoria_filter, usuario=user)
        
        else: #si el usuario no ha seleccionado filtros:
            queryset = queryset.filter(usuario=user)

        return queryset
    def post(self, request, *args, **kwargs): #override de post de la clase padre (ListView)
        tarea_id = request.POST.get('tarea_id') #obtiene el tarea_ide de los parámetros del POST, cada vez que se presiona "Completar" o "Eliminar"
        tarea = Tarea.objects.get(id=tarea_id) #obtiene el objeto Tarea asociado al tarea_id obtenido en la línea anterior.

        if 'estado' in request.POST: #si en el POST viene un campo 'estado':
            tarea.estado = request.POST['estado'] #actualiza el campo con el valor correspondiente
        elif 'categoria' in request.POST: #si en el POST viene un campo 'categoría':
            tarea.categoría = request.POST['categoria'] #acrualiza el campo con el valor correspondiente
        
        tarea.save() #guarda
        return redirect('tareas-list') #redirige al listview, reflejándose el cambio de inmediato.

def pedido_manual(request):
    form = pedidos_manuales()

    if request.method == "POST":
        print(request)
        form = pedidos_manuales(request.POST)

        if form.is_valid():
            print(form)
            pedido = Pedido()
            pedido.cliente_solicitante = form.cleaned_data['cliente_solicitante']
            pedido.producto = form.cleaned_data['productos']
            #pedido.numero_transaccion = #pull highest number in database + 1
            #pedido.subtotal = sum(producto.precio for producto in form.cleaned_data['productos'])
            #-- estimar numero de orden
            #--falla si está vacío    
            if Pedido.objects.exists():
                ultimo_pedido = Pedido.objects.latest('numero_transaccion')
                pedido.numero_transaccion = ultimo_pedido.numero_transaccion + 1
            else:
                pedido.numero_transaccion = 1
            pedido.subtotal = pedido.productos.precio
            pedido.fecha_pedido = datetime.datetime.now()
            pedido.save()
            messages.success(request, 'Pedido ingresado exitosamente')
        else:
            print("Datos invalidos")
        return redirect('pedido_manual')
    context = {
        'form': form
    }
    return render(request, 'compraventa/pedidos.html', context=context)

def pedido_manual_cliente(request):
    form = pedidos_manuales_cliente()
    if request.method == "POST":
        form = pedidos_manuales_cliente(request.POST)
        if form.is_valid():
            pedido = Pedido()
            try:
                cliente = Cliente.objects.get(user=request.user)
                pedido.cliente_solicitante = cliente
            except Cliente.DoesNotExist:
                raise ValueError("No se encuentra el cliente de origen")

            productos = form.cleaned_data['productos']
            selected_productos = list(productos) 
            pedido.productos.set(selected_productos)

            #for producto in productos:
            #    print(producto)
            #    pedido.productos.set(producto)
            #pedido.productos = form.cleaned_data['productos']
            #aparentemnete tendremos que hacer producto.set()
            pedido.tiene_despacho = form.cleaned_data['tiene_despacho']
            pedido.subtotal = pedido.productos.precio
            pedido.fecha_pedido = datetime.datetime.now()
            pedido.save()
            messages.success(request, 'Pedido ingresado exitosamente')
        else:
            print("Datos invalidos")
        return redirect('pedido_manual_cliente')
    context = {
        'form': form
    }
    return render(request, 'compraventa/pedidos externos.html', context=context)
"""



     