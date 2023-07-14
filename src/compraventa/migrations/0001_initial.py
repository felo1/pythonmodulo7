# Generated by Django 4.2.2 on 2023-07-05 01:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=11, unique=True)),
                ('telefono_movil', models.CharField(blank=True, default='', max_length=30)),
                ('notas', models.CharField(blank=True, default='', max_length=250)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(default='', max_length=250)),
                ('usuario', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='compraventa.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('direccion', models.CharField(default='', max_length=250)),
                ('ciudad', models.CharField(choices=[('VDM', 'Viña del Mar'), ('STGO', 'Santiago'), ('ETC', 'Etcétera')], default='VDM', max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('nombre', models.CharField(max_length=30)),
                ('precio', models.IntegerField(default=1)),
                ('sku', models.AutoField(primary_key=True, serialize=False)),
                ('stock', models.IntegerField(default=0)),
                ('modelo', models.CharField(default=None, max_length=250)),
                ('impuesto', models.FloatField(default=19, verbose_name='IVA')),
                ('descuento', models.FloatField(default=0)),
                ('categoria', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='compraventa.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('numero_transaccion', models.AutoField(primary_key=True, serialize=False)),
                ('subtotal', models.FloatField(default=0, verbose_name='Subtotal')),
                ('suma_descuentos', models.FloatField(default=0, verbose_name='Descuentos')),
                ('total_pedido', models.FloatField(default=0, verbose_name='Total a pagar')),
                ('fecha_pedido', models.DateTimeField(default='2023-1-1')),
                ('estado_despacho', models.CharField(choices=[('Recibido', 'Recibido'), ('Pago aceptado', 'Pago aceptado'), ('Orden de compra generada', 'Orden de compra generada'), ('En proceso', 'En proceso'), ('Enviado', 'Enviado'), ('En transito', 'En transito'), ('Entregado', 'Entregado')], default='Recibido', max_length=30)),
                ('cliente_solicitante', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='compraventa.cliente')),
                ('direccion_despacho', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='compraventa.direccion')),
                ('productos', models.ManyToManyField(default=None, to='compraventa.producto')),
            ],
        ),
    ]