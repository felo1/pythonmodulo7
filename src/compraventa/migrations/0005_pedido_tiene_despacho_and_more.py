# Generated by Django 4.2.2 on 2023-07-07 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compraventa', '0004_alter_pedido_cliente_solicitante'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='tiene_despacho',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='direccion_despacho',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='compraventa.direccion'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='estado_despacho',
            field=models.CharField(choices=[('Recibido', 'Recibido'), ('Pago aceptado', 'Pago aceptado'), ('Orden de compra generada', 'Orden de compra generada'), ('En proceso', 'En proceso'), ('Enviado', 'Enviado'), ('En transito', 'En transito'), ('Entregado', 'Entregado')], default='Recibido', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='fecha_pedido',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
