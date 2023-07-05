from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Categoria(models.Model):
    nombre = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre
    
#considerar categoria padre e hija, como implementar esto?
class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField(default=1)
    sku = models.AutoField(primary_key=True)
    stock = models.IntegerField(default=0)
    modelo = models.CharField(max_length=250, default=None) 
    #deberá ser llenado de forma que se pueda parsear para presentar el contenido. 
    #cual sería la mejor manera de lidiar con esto?
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, default=None)
    impuesto = models.FloatField(default=19, verbose_name="IVA")
    descuento = models.FloatField(default=0) # descuento base + descuentos circunstanciales

    def __str__(self):
        return 'sku: ' + str(self.sku) + ' | ' + self.nombre

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
    #ver como restringiur modificar algunas cosas que en un producto de la vida real no deberian ser
    #modificables en la administracion una vez generado un pedido.
    cliente_solicitante = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, default=None)
    productos = models.ManyToManyField(Producto, default=None)
    #ver alguna forma de almacenar numeros de boleta de fantasia que no intervengan con 
    #el ingreso de los productos en los pedidos
    #posiblemente con shortUID como mencionó anibal (para generar IDs publoicos aleatorios)
    #si funcionan como index SIN ser el ID, que es algo de uso interno
    numero_transaccion = models.AutoField(primary_key=True) # n° de orden de compra
    #para trazabilidad de la info.
    subtotal = models.FloatField(default=0, verbose_name="Subtotal")
    suma_descuentos = models.FloatField(default=0, verbose_name="Descuentos") # sumatoria de los descuentos individuales
    total_pedido = models.FloatField(default=0, verbose_name="Total a pagar") # monto a pagar, descuentos e intereses
    fecha_pedido = models.DateTimeField()
    tiene_despacho = models.BooleanField
    ESTADO_CHOICES = [
        ('Recibido', 'Recibido'),
        ('Pago aceptado', 'Pago aceptado'),
        ('Orden de compra generada', 'Orden de compra generada'),
        ('En proceso', 'En proceso'),
        ('Enviado', 'Enviado'),
        ('En transito', 'En transito'),
        ('Entregado', 'Entregado'),
    ]
    estado_despacho = models.CharField(max_length=30, choices=ESTADO_CHOICES, default="Recibido", blank=False)
    direccion_despacho = models.ForeignKey(Direccion, on_delete=models.DO_NOTHING)

    def __str__(self):
        return 'Orden de compra N°: ' + str(self.numero_transaccion) + ' | Nombre de cliente: '+ self.cliente_solicitante.nombres + ' ' + self.cliente_solicitante.apellidos + " | Estado de despacho: " + self.estado_despacho
    
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
