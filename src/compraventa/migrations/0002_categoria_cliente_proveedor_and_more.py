# Generated by Django 4.2.2 on 2023-06-27 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compraventa', '0001_initial'),
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
                ('nombres', models.CharField(max_length=30)),
                ('apellidos', models.CharField(max_length=30)),
                ('rut', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='numero_transaccion',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='pedido',
            name='subtotal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pedido',
            name='suma_descuentos',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='pedido',
            name='total_pedido',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='descuento',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='impuesto',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='modelo',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AddField(
            model_name='producto',
            name='precio',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(default=0),
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='cliente_solicitante',
        ),
        migrations.AddField(
            model_name='producto',
            name='categoria',
            field=models.ManyToManyField(to='compraventa.categoria'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='cliente_solicitante',
            field=models.ManyToManyField(to='compraventa.cliente'),
        ),
    ]