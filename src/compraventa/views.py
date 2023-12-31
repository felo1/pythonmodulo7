
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic import UpdateView, DetailView
from django.shortcuts import render
from .models import Categoria, Cliente, Pedido, Producto, ItemPedido
from .forms import RegistrarUsuarioForm, PedidoForm, ItemPedidoForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.sessions.models import Session #manejo de sesiones
#from .forms import pedidos_manuales, pedidos_manuales_cliente
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, User
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied #para evitar que administrativos entren como clientes con links directos

# Create your views here.
#clon de Gestionplview pa que clientes puedan ver sus pedidos
#los mixins deben ir antes de las vistas que los requieren (classic paiton)
class SoloStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        print("User authenticated:", self.request.user.is_authenticated)
        print("User is staff:", self.request.user.is_staff)
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, "Acceso restringido, favor usar su cuenta administrativa")
        return redirect(reverse('login'))
    
    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
class ExcluirStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, "Página restringida para administrativos o usuarios no identificados")
        return redirect(reverse('login'))
    
    def dispatch(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
#TODO: falta que el usuario pueda volver a esta vista si hace click en el logo 
def index(request):
        usuario = request.user.id
       
        pedidos = Pedido.objects.all();
        #pedidos = Pedido.objects.filter(usuario=request.user).order_by('id_pedido')
        return render(request, 'compraventa/pedido_list_cliente.html', {'pedidos': pedidos}) #== esta dando 1
        #pedidos = Pedido.objects.filter(usuario=request.user).order_by('id_pedido')
    #return render(request, 'compraventa/index.html')

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
        if form.is_valid():
            
            user = form.save() #guardar formulario
            try:
                grupo = Group.objects.get(name='usuario_cliente')  # buscar el grupo
                user.groups.add(grupo)  # asignarlo al usuario
            except ObjectDoesNotExist:
                #En el caso de que en revisión no creen el grupo primero:
                grupo = Group.objects.create(name='usuario_cliente')
                user.groups.add(grupo)  # asignarlo al usuario    

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

class ProductoListView(LoginRequiredMixin, ListView): #endpoint agregar al carrito, lado usuario común
    model = Producto
    #paginate_by = 10 para usar falta implementar en template
 
    def get_context_data(self, **kwargs): #override del método de la clase padre, que es un generador de contexto para pasarlo al template
        context = super().get_context_data(**kwargs) #llama al método de la clase padre ListView usando super()
        pedido_form = PedidoForm() #se instancia un formulario PedidoForm vacío
        itempedido_form = ItemPedidoForm() #formulario vacío
        context['pedido_form'] = pedido_form #se agrega pedido_form a la lista de contextos
        context['itempedido_form'] = itempedido_form #y el otro form
        context['cliente_id']  = Cliente.objects.get(user_id=self.request.user.id)
        context['id_pedido'] = self.request.session.session_key #session key es el nro de pedido en los pedidos realizados por el cliente
        
       
        return context #lista de contextos final
    
    def post(self, request, *args, **kwargs): #override de post de la clase padre (ListView).
        #este método utiliza condiciones lógicas sobre el contenido del POST, para decidir qué se hace con la información.
        
        if not request.session.session_key: #asegurarse de que exista sesión y que tenga asignada un session_key (en SOF decía que podía darse el caso)
            request.session.save()
        session_id = request.session.session_key #obtiene session_key, para asignarlo luego a pk de Pedido
      
        user_id = request.user.id #id de usuario logueado
       
        self.cliente_id = Cliente.objects.get(user_id=user_id) #obtiene el cliente a partir del usuario, recordar que cliente tiene
        #relación 1 a 1 con un usuario.

        pedido = Pedido.objects.filter(id_pedido=session_id).exists() #devuelve True si existe un pedido con un id_pedido = session_key,
        
        # el que podría existir si es que ya se generó instancias de ItemPedido al haber agregado itemes al carrito
        print("pedido exists", pedido)
        print("id pedido dentro de post---------------", Pedido.objects.get(id_pedido=session_id))
        if not pedido: #si no hay un pedido
            Pedido.objects.create(id_pedido=session_id, cliente_solicitante=self.cliente_id) #crea uno
        pedido = Pedido.objects.get(cliente_solicitante=self.cliente_id, id_pedido=session_id) #finalmente, asigna un objeto Pedido a la variable pedido
        if 'cantidad' in request.POST: #si en el POST viene un campo 'cantidad':
         
            self.contexto_pedido = pedido
            cantidad = request.POST['cantidad'] #obtiene la cantidad desde el POST
            id_producto = request.POST['id_producto'] #obtiene el id_producto desde el POST
            producto = Producto.objects.get(id_producto=id_producto) #obtiene instancia del producto agregado y la asigna a 'producto'
            item_pedido = ItemPedido.objects.create(cantidad=cantidad, pedido=pedido, producto=producto) #lo mismo con item_pedido
            
            item_pedido.save() #y guarda
        
            
    
        item_pedido.save() #guarda
        return redirect('productos') #redirige al listview, reflejándose el cambio de inmediato.
 

class ClientePedidoListView(ExcluirStaffMixin, ListView):
    model = Pedido
    paginate_by = 10
    template_name = 'compraventa/pedido_list_cliente.html'
  
    #cliente_id = Cliente.objects.get(user_id=user_id)
    #este tryexcept es necesario para evitar que la falta de cliente como parte del perfil del usuario staff crashee la  vista antes de que el mixin pueda entrar en efecto.
    def get_queryset(self):
        try:
            queryset = super().get_queryset()
            usuario = self.request.user.id
            cliente = Cliente.objects.get(user_id=usuario)
            queryset = Pedido.objects.filter(cliente_solicitante=cliente).order_by('-fecha_pedido')
            return queryset
        except Cliente.DoesNotExist:
            messages.error(self.request, "Usuario conectado no tiene un perfil de cliente asociado. ¿Está usando una cuenta administrativa?")
            raise PermissionDenied()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pedidos"] = Pedido.objects.all()
        ##################intento de pasarle el estado_despacho al template como un string.
        #primero convertimos el query a una lista de diccionarios:
        #pedido_list = list(Pedido.objects.all().values())
        
        #luego, cad item de diccionario lo agregamos al context:
    
        #for item in pedido_list:
        #context["pedidos"] = item

        print("--------------------context:", context)
        return context

    def post(self, request, *args, **kwargs): #override de post de la clase padre (ListView).
        #pedidos = Pedido.objects.all #todos los pedidos

        id_pedido = request.POST.get('pedido') #asigna el id_pedido que viene en el post a una variable
        pedido = Producto.objects.get(id_pedido=id_pedido) #obtiene instancia del pedido a modificar y la asigna a 'pedido'
        pedido.id_pedido = request.POST['id_pedido'] #obtiene el id_pedido desde el POST y le hace un update
        pedido.save() #guarda
        return redirect('edit_pedido') #redirige al listview, reflejándose el cambio de inmediato.

class GestiónPedidoListView(SoloStaffMixin, LoginRequiredMixin, ListView):
    model = Pedido
    paginate_by = 10 #https://docs.djangoproject.com/en/4.2/topics/pagination/#paginating-a-listview
    template_name = 'compraventa/pedido_list_gestion.html'
    
    def get_queryset(self): #override del método de la clase padre para obtener los queryset que necesitemos para dar la funcionalidad de filtrado
        queryset = super().get_queryset() #super() a la clase padre, para obtener el queryset inicial
    
        tiene_despacho_filter = self.request.GET.get('tiene_despacho_filter')
        estado_despacho_filter = self.request.GET.get('estado_despacho_filter') #si se ha seleccionado un filtro de estado, se asigna a esta variable
        
        #cliente = self.request.user #se asigna el usuario logueado a una variable para usarlo más abajo.
        #si se cumplen las siguientes pruebas lógicas, se realiza un queryset con los parámetros indicados por los choicefields:

        if estado_despacho_filter and tiene_despacho_filter: # si el usuario ha filtrado por estado Y categoría            
            queryset = queryset.filter(estado_despacho=estado_despacho_filter, tiene_despacho=tiene_despacho_filter).order_by('-fecha_pedido')
             
        elif estado_despacho_filter: # si el usuario ha filtrado sólo por estado,
            # Filtering by estado only
            queryset = queryset.filter(estado_despacho=estado_despacho_filter).order_by('-fecha_pedido')
        elif tiene_despacho_filter: # si el usuario ha filtrado sólo por categoría,
            # Filtering by categoria only
            queryset = queryset.filter(tiene_despacho=tiene_despacho_filter).order_by('-fecha_pedido')
        
        else: #si el usuario no ha seleccionado filtros:
            queryset = Pedido.objects.all().order_by('-fecha_pedido')

        return queryset
 
    def get_context_data(self, **kwargs): #override del método de la clase padre, que es un generador de contexto para pasarlo al template
        context = super().get_context_data(**kwargs) #llama al método de la clase padre ListView usando super()
        pedido_form = PedidoForm() #se instancia un formulario PedidoForm vacío
        itempedido_form = ItemPedidoForm() #formulario vacío
        context['pedido_form'] = pedido_form #se agrega pedido_form a la lista de contextos
        context['itempedido_form'] = itempedido_form #y el otro form
        return context #lista de contextos final   
    
    def post(self, request, *args, **kwargs): #override de post de la clase padre (ListView).
        #pedidos = Pedido.objects.all #todos los pedidos

      
        if 'estado_despacho' in request.POST: #si en el POST viene un campo 'estado_despacho':
            id_pedido = request.POST.get('id_pedido') #asigna el id_pedido que viene en el post a una variable
            pedido = Pedido.objects.get(id_pedido=id_pedido) #obtiene instancia del pedido a modificar y la asigna a 'pedido'
            pedido.id_pedido = request.POST['id_pedido'] #obtiene el id_pedido desde el POST y le hace un update
         
        else:
            pedido.save()
    
        pedido.save() #guarda
        return redirect('gestion-pedidos') #redirige al listview, reflejándose el cambio de inmediato.
 

class TomarPedidoListView(ListView): #LE SAQUÉ SOLOSTAFFMIXIN
    model = Producto
    #paginate_by = 10 para usar falta implementar en template
 
    def get_queryset(self):
    
        self.id_pedido_actual = self.request.GET.get('id_pedido')
        self.cliente_actual = self.request.GET.get('cliente_elegido')
        self.queryset['id_pedido'] = self.id_pedido_actual
        self.queryset['cliente_elegido'] = self.cliente_actual
        print("queryset-------------------------", self.queryset)

        return self.queryset
    
    def get_context_data(self, **kwargs): #override del método de la clase padre, que es un generador de contexto para pasarlo al template
        context = super().get_context_data(**kwargs) #llama al método de la clase padre ListView usando super()
        pedido_form = PedidoForm() #se instancia un formulario PedidoForm vacío
        itempedido_form = ItemPedidoForm() #formulario vacío
        context['pedido_form'] = pedido_form #se agrega pedido_form a la lista de contextos
        context['itempedido_form'] = itempedido_form #y el otro form
        print("session id-----------------", self.session.user.id)
        cliente_actual = Cliente.objects.get(user_id = self.session.user.id)
        context['id_cliente_pedido'] = cliente_actual
        print("context-------------------", context)
        return context #lista de contextos final   
    
    def post(self, request, *args, **kwargs): #override de post de la clase padre (ListView).
        #este método utiliza condiciones lógicas sobre el contenido del POST, para decidir qué se hace con la información.

        if not request.session.session_key: #asegurarse de que exista sesión y que tenga asignada un session_key (en SOF decía que podía darse el caso)
            request.session.save()
        session_id = request.session.session_key #obtiene session_key, para asignarlo luego a pk de Pedido
      
        user_id = request.user.id #id de usuario logueado
       
        cliente_id = Cliente.objects.get(user_id=user_id) #obtiene el cliente a partir del usuario, recordar que cliente tiene
        #relación 1 a 1 con un usuario.

        pedido = Pedido.objects.filter(id_pedido=session_id).exists() #devuelve True si existe un pedido con un id_pedido = session_key,
        # el que podría existir si es que ya se generó instancias de ItemPedido al haber agregado itemes al carrito

        if not pedido: #si no hay un pedido
            Pedido.objects.create(id_pedido=session_id, cliente_solicitante=cliente_id) #crea uno
        pedido = Pedido.objects.get(cliente_solicitante=cliente_id, id_pedido=session_id) #finalmente, asigna un objeto Pedido a la variable pedido

        if 'cantidad' in request.POST: #si en el POST viene un campo 'cantidad':
         
            cantidad = request.POST['cantidad'] #obtiene la cantidad desde el POST
            id_producto = request.POST['id_producto'] #obtiene el id_producto desde el POST
            producto = Producto.objects.get(id_producto=id_producto) #obtiene instancia del producto agregado y la asigna a 'producto'
            item_pedido = ItemPedido.objects.create(cantidad=cantidad, pedido=pedido, producto=producto) #lo mismo con item_pedido
            item_pedido.save() #y guarda   
    
        item_pedido.save() #guarda
        return redirect('productos') #redirige al listview, reflejándose el cambio de inmediato.

@login_required
def buscar_usuario(request):
    if request.method == "POST":
        búsqueda_usuario = request.POST['búsqueda_usuario']
        nombres_encontrados = Cliente.objects.filter(nombres__icontains=búsqueda_usuario)
        apellidos_encontrados = Cliente.objects.filter(apellidos__icontains=búsqueda_usuario)
        ruts_encontrados = Cliente.objects.filter(rut__icontains=búsqueda_usuario)
        encontrados = nombres_encontrados | ruts_encontrados | apellidos_encontrados
        return render(request, 'compraventa/tomar_pedido.html', {'búsqueda_usuario':búsqueda_usuario, 'encontrados':encontrados})
    
    else:
        return render(request, 'compraventa/tomar_pedido.html', {})
    
@login_required
def tomar_pedido_paso2(request):
        
    if request.method == "GET":
        cliente_elegido = request.GET['id_cliente']
        uuid_pedido = uuid.uuid1() #se genera un uuid, que si se confirma la creación de un pedido se asignará posteriormente
        #como id_pedido y se entregará en el GET al tomar_pedido_paso3
        return render(request, 'compraventa/tomar_pedido_paso2.html', {'cliente_elegido':cliente_elegido, 'uuid_pedido':uuid_pedido})

    else:
        return render(request, 'compraventa/tomar_pedido_paso2.html', {})
    
#@login_required
class Tomar_pedido_paso3(ListView): #le saqué temporalemente solostaffmixin

    model = Producto
    paginate_by = 10
    template_name = 'compraventa/tomar_pedido_paso3.html'

    def get_queryset(self):
        global id_pedido_actual #para poder usar la variable en el método get_context_data. se le pone un nombre distinto para evitar
        #toparse con otros id_pedido de otras partes del código
        global cliente_actual # lo mismo
        id_pedido_actual = self.request.GET.get('id_pedido')
        cliente_actual = self.request.GET.get('cliente_elegido')
        queryset = Producto.objects.all()
        return queryset
        
 
    def get_context_data(self, **kwargs): #override del método de la clase padre, que es un generador de contexto para pasarlo al template
        global context
        context = super().get_context_data(**kwargs) #llama al método de la clase padre ListView usando super()
        pedido_form = PedidoForm() #se instancia un formulario PedidoForm vacío
        itempedido_form = ItemPedidoForm() #formulario vacío
        print("-------------------context: ", context)
        cliente_actual = self.request.GET.get('cliente_elegido')
        objeto_cliente_actual = Cliente.objects.get(id=cliente_actual) #como cliente_actual es solo el número, se crea esto para obtener otros datos, como nombres
        context['pedido_form'] = pedido_form #se agrega pedido_form a la lista de contextos
        context['itempedido_form'] = itempedido_form #y el otro form
        context['id_pedido'] = id_pedido_actual #se asigna desde la variable global generada en el método get_queryset
        context['cliente_actual'] = cliente_actual
        context['objeto_cliente_actual'] = objeto_cliente_actual
        return context #lista de contextos final   
    
    def post(self, request, *args, **kwargs): #override de post de la clase padre (ListView).
        #este método utiliza condiciones lógicas sobre el contenido del POST, para decidir qué se hace con la información.
        
        
        pedido = Pedido.objects.filter(id_pedido=id_pedido_actual).exists() #devuelve True si existe un pedido con un id_pedido = session_key,
        # el que podría existir si es que ya se generó instancias de ItemPedido al haber agregado itemes al carrito

        if not pedido: #si no hay un pedido
            cliente = Cliente.objects.get(id = cliente_actual)
            Pedido.objects.create(id_pedido=id_pedido_actual, cliente_solicitante=cliente) #crea uno
        pedido = Pedido.objects.get(cliente_solicitante=cliente_actual, id_pedido=id_pedido_actual) #finalmente, asigna un objeto Pedido a la variable pedido
    
        if 'cantidad' in request.POST: #si en el POST viene un campo 'cantidad':
         
            cantidad = request.POST['cantidad'] #obtiene la cantidad desde el POST
            id_producto = request.POST['id_producto'] #obtiene el id_producto desde el POST
            producto = Producto.objects.get(id_producto=id_producto) #obtiene instancia del producto agregado y la asigna a 'producto'
            item_pedido = ItemPedido.objects.create(cantidad=cantidad, pedido=pedido, producto=producto) #lo mismo con item_pedido
            
            item_pedido.save() #y guarda   
            return render(request, 'compraventa/tomar_pedido_paso3.html', context=context)
        if 'id_pedido_ok' in request.POST:
            return render(request, 'compraventa/tomar_pedido_paso4.html', {'id_pedido': request.POST['id_pedido_ok']})
        
        #item_pedido.save() #guarda
        return render(request, 'compraventa/tomar_pedido_paso3.html', {})
     
class PedidoEditView( UpdateView): #Updateview es un class-based view usado para actualizar datos #solostaffmixin se sacó
    model = Pedido #se elige el modelo
    form_class = PedidoForm #se elige el formulario
    template_name = "compraventa/edit_pedido.html" #se elige el template

    def get_success_url(self): #override del metodo que la clase usa al completar exitosamente la edición. En este paso redirige al list-view
        return reverse('gestion-pedidos')

    def get_object(self, queryset=None): #override del método de la clase padre.
        pedido = super().get_object(queryset) #obtiene el objeto pedido y lo asigna a esta variable
       
        pedido.save() #se guarda
        return pedido
    
class ClientePedidoEditView(DetailView):
    model = Pedido
    template_name = "compraventa/detalle_pedido.html"
    pk_url_kwarg = 'pk'  # Specify the keyword argument for the primary key

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data if needed
        return context

from django.views import View
class CancelarPedidoView(View):
    def post(self, request, pk):
        pedido = Pedido.objects.get(pk=pk)
        pedido.estado_despacho = request.POST.get('estado_despacho')
        pedido.save()
        return HttpResponseRedirect(reverse('detalle_pedido', args=[pk]))
    

class TomarPedidoPaso4View(ListView):
    template_name = 'compraventa/tomar_pedido_paso4.html'
    context_object_name = 'pedidos'
   
    
    def get_queryset(self):

        self.id_pedido = self.request.GET.get('id_pedido')
        print("id_pedido---------:", self.id_pedido)
        queryset = ItemPedido.objects.filter(pedido_id = self.id_pedido)
        """
        try:
            pedido = Pedido.objects.get(id_pedido=id_pedido)
            itempedidos = ItemPedido.objects.filter(pedido_id =)
        except Pedido.DoesNotExist:
            # Handle the case when the pedido doesn't exist
            pedido = None
            productos = []
        """
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("self get", self.get)
        id_pedido = self.id_pedido
        try:
            pedido = Pedido.objects.get(id_pedido=id_pedido)
        except Pedido.DoesNotExist:
            pedido = None
        context['productos'] = ItemPedido.objects.filter(pedido_id=id_pedido)
        context['pedido'] = pedido
        return context
    
    def post(self, request, *args, **kwargs):
        if 'id_pedido_ok' in request.POST:
            id_pedido = request.POST['id_pedido_ok'] #obtiene el id del pedido ya terminado
            return render(request, 'compraventa/tomar_pedido_paso4.html', {'id_pedido' : id_pedido})



"""

Request Method:	POST
Request URL:	http://127.0.0.1:8000/pedidos/1/edit/
Django Version:	4.2.2
Exception Type:	NoReverseMatch
Exception Value:	
Reverse for 'pedido-list' not found. 'pedido-list' is not a valid view function or pattern name.

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



     