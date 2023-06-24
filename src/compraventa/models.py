from django.db import models

# Create your models here.

class Producto(models.Model):
    ##first_name = models.CharField(max_length=30)
    #last_name = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField
    sku = models.CharField(max_length=15)
    #stock, por sucursal? 
    #proveedor, tabla intermedia?
    #modelo = models.Choices (?, que guarde una lista)
    #categoria M:M,
    #proveedor M:M
    #impuesto

class Pedido(models.Model):
    cliente_solicitante = models.CharField #foreignKey cliente pendiente
    #foreign key tabla intermedia con productos (M:M)
    numero_pedido = models.IntegerField #n° de orden de compra
    suma_por_producto = models.FloatField #sumatoria de producto individual x cantidad. M:M? Cómo será la lógica?
    descuento_porcentual = models.IntegerChoices
    total_pedido = models.FloatField #monto a pagar, descuentos & intereses