Trabajos grupales Módulo 7
--------------
AE 1
--------------
✔ Crear un proyecto en Django, con las aplicaciones que estimes necesarias para abordar el
problema anterior.

    Nuestra app se llama 'compraventa' (http://127.0.0.1:8000/) y 
    se encuentra dentro del proyecto 'proyecto'

✔ Conectar el proyecto a una base de datos en PostgreSQL

    Según lo conversado con awakers, por el momento se trabajará en 
    SQLite para poder trabajar en máquinas distintas


✔ Realizar la migración inicial, corroborando que ésta se ve reflejada en la base de datos
PostgreSQL.

    Se realiza migraciones en SQLite3:

    ![Image](https://raw.githubusercontent.com/rodrigolfh/pythonmodulo7/main/img_readme/base.png)




- Definir usuarios de tipo superuser y usuarios del sistema, considerando que todos podrán
interactuar con sus propias tareas.

- La página principal será una página con datos e información básica de “Te lo vendo”. En esta
ventana abordaremos el RFW-002, debiendo existir un formulario de Login para los usuarios
comunes que puedan ingresar a las funcionalidades de sus pedidos como clientes en área web.
Deberá llevar a página simple que dé la bienvenida, la que se trabajará posteriormente
dependiendo del rol del usuario.
- Definir la documentación necesaria para el modelo de datos físico, a partir del cual trabajará la
definición de sus modelos de Django. Éste deberá ser validado con tu Awaker o Adviser.