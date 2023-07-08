from django.db.models import Sum

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

impuesto = 19

class Categoria(models.Model):
    nombre = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre
    
#considerar categoria padre e hija, como implementar esto?
class Producto(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=256, null=True)
    precio = models.IntegerField(default=1)    
    stock = models.IntegerField(default=0)
    modelo = models.CharField(max_length=250, default=None) 
    #deberá ser llenado de forma que se pueda parsear para presentar el contenido. 
    #cual sería la mejor manera de lidiar con esto?
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, default=None)
    #impuesto = models.FloatField(default=19, verbose_name="IVA")
    descuento = models.FloatField(default=0) # descuento base + descuentos circunstanciales

    def __str__(self):
        return 'sku: ' + str(self.id_producto) + ' | ' + self.nombre

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) 
    rut = models.CharField(max_length=11, unique=True)
    nombres = models.CharField(max_length=15, default="", blank=True)
    apellidos =  models.CharField(max_length=15, default="", blank=True)
    telefono_fijo = models.CharField(max_length=15, default="", blank=True)
    telefono_movil = models.CharField(max_length=30, default="", blank=True)
    notas = models.CharField(max_length=250, default="", blank=True)
    #direcciones = models.ManyToManyField(Direccion, max_length=100, default="", blank=True)

    def __str__(self):
        return self.nombres + ' ' + self.apellidos
    
class Direccion(models.Model):
    direccion = models.CharField(max_length=250, default="")
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE, default=None)
    def __str__(self) -> str:
        return self.direccion
    

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cliente_solicitante = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, default=None)
    fecha_pedido = models.DateTimeField(auto_now=True, null=True)
    tiene_despacho = models.BooleanField(null=True)
    ESTADO_CHOICES = [
        ('Recibido', 'Recibido'),
        ('Pago aceptado', 'Pago aceptado'),
        ('Orden de compra generada', 'Orden de compra generada'),
        ('En proceso', 'En proceso'),
        ('Enviado', 'Enviado'),
        ('En transito', 'En transito'),
        ('Entregado', 'Entregado'),
    ]
    estado_despacho = models.CharField(max_length=30, choices=ESTADO_CHOICES, default="Recibido", null=True)
    direccion_despacho = models.ForeignKey(Direccion, on_delete=models.DO_NOTHING, null=True)
    impuesto = models.IntegerField(default=19)

    def subtotal(self):
        return self.itempedido_set.aggregate(total=Sum('precio'))['total'] or 0

    def total_pedido(self):
        subtotal = self.subtotal()
        total_con_impuesto = subtotal + (subtotal * self.impuesto / 100)
        return round(total_con_impuesto)
    
    def __str__(self):
        return 'Orden de compra N°: ' + str(self.id_pedido) + ' | Nombre de cliente: '+ self.cliente_solicitante.nombres + ' ' + self.cliente_solicitante.apellidos + " | Estado de despacho: " + self.estado_despacho

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.DO_NOTHING, related_name='itempedido_set')
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField(default=1)

    # Other fields and methods for the ItemPedido model




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
