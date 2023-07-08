from django.contrib.auth.models import User
from compraventa.models import Producto, Cliente
from faker import Faker
import random
import string

fake = Faker('es_ES')

for _ in range(10):
    nombre = fake.word()
    descripcion = fake.sentence()
    precio = random.randint(100, 1000)
    stock = random.randint(0, 100)
    modelo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    producto = Producto.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock,
        modelo=modelo
    )

for _ in range(10):
    user = User.objects.create_user(
        username=fake.unique.user_name(),
        password='contraseña',
        email=fake.email()
    )
    rut = fake.unique.rut()
    nombres = fake.first_name()
    apellidos = fake.last_name()
    telefono_fijo = fake.phone_number()
    telefono_movil = fake.phone_number()
    notas = fake.sentence()

    cliente = Cliente.objects.create(
        user=user,
        rut=rut,
        nombres=nombres,
        apellidos=apellidos,
        telefono_fijo=telefono_fijo,
        telefono_movil=telefono_movil,
        notas=notas
    )
