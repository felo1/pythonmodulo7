from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Categoria(models.Model):
    nombre = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre
    
#considerar categoria padre e hija, como implementar esto?

class Proveedor(models.Model):
    nombre = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField(default=1)
    sku = models.CharField(max_length=15)
    stock = models.IntegerField(default=0) # Stock per sucursal
    #proveedor = models.ForeignKey('Proveedor', blank=True)  # 
    modelo = models.CharField(max_length=250, default=None) #deberá ser llenado de forma que se pueda parsear para presentar el contenido. 
    #cual sería la mejor manera de lidiar con esto?
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, default=None)
    impuesto = models.FloatField(default=0)
    descuento = models.FloatField(default=0) # descuento base + descuentos circunstanciales

    def __str__(self):
        return 'sku: ' + self.sku + ' | ' + self.nombre

#modificar la clase cliente para que sea una extensión del usuario base, para aprovechar las funcionalidades
#que tendrá prontamente de login (para acceder a menu de transacciones históricas, despachos pendientes, etc), etc.
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) #uno a uno cliente con usuario, importante agregar primary key
    #para que se vea en el admin, se modifica también el admin.py
    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    rut = models.CharField(max_length=11)
    telefono_movil = models.CharField(max_length=30, default="", blank=True)
    telefono_fijo = models.CharField(max_length=30, default="", blank=True)  
    notas = models.CharField(max_length=250, default="", blank=True)
    direcciones = models.CharField(max_length=250, default="", blank=True)

    def __str__(self):
        return self.nombres + ' ' + self.apellidos

class Pedido(models.Model):
    cliente_solicitante = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, default=None)
    productos = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, default=None)
    numero_transaccion = models.IntegerField(default=0) # n° de orden de compra
    #para trazabilidad de la info.
    subtotal = models.FloatField(default=0)
    suma_descuentos = models.FloatField(default=0) # sumatoria de los descuentos individuales
    total_pedido = models.FloatField(default=0) # monto a pagar, descuentos e intereses
    fecha_pedido = models.DateTimeField(default='2023-1-1')
    tiene_despacho = models.BooleanField
    #TODO: estado despacho debe ser un selector

    ESTADO_CHOICES = [
        ('Recibido', 'Recibido'),
        ('Pago aceptado', 'Pago aceptado'),
        ('Orden de compra generada', 'Orden de compra generada'),
        ('En proceso', 'En proceso'),
        ('Enviado', 'Enviado'),
        ('En transito', 'En transito'),
        ('Despachado', 'Despachado'),
    ]
    estado_despacho = models.CharField(max_length=30, choices=ESTADO_CHOICES, default="Recibido", blank=False)
    direccion = models.CharField(max_length=250, default="")

    def __str__(self):
        return str(self.numero_transaccion)
    
class Sucursal(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=250, default="")

    class Ciudad(models.TextChoices):
        VDM = 'VDM', 'Viña del Mar'
        STGO = 'STGO', 'Santiago'
        ETC = 'ETC', 'Etcétera'
    
    ciudad = models.CharField(
        max_length=4,
        choices=Ciudad.choices,
        default=Ciudad.VDM 
    )

    def __str__(self):
        return self.nombre
