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



✔ Definir usuarios de tipo superuser y usuarios del sistema, considerando que todos podrán
interactuar con sus propias tareas.

    admin:admin
    rodrigo:contraseña

![Image](https://raw.githubusercontent.com/rodrigolfh/pythonmodulo7/main/img_readme/usuarios.png)



✔ La página principal será una página con datos e información básica de “Te lo vendo”.

    http://127.0.0.1:8000/

✔ En esta ventana abordaremos el RFW-002, debiendo existir un formulario de Login para los usuarios
comunes que puedan ingresar a las funcionalidades de sus pedidos como clientes en área web.

    http://127.0.0.1:8000/login

✔ Deberá llevar a página simple que dé la bienvenida, la que se trabajará posteriormente
dependiendo del rol del usuario.

![Image](https://raw.githubusercontent.com/rodrigolfh/pythonmodulo7/main/img_readme/hola.png)


✔ Definir la documentación necesaria para el modelo de datos físico, a partir del cual trabajará la
definición de sus modelos de Django. Éste deberá ser validado con tu Awaker o Adviser.



--------------
AE2
--------------

 Crear los modelos de datos correspondientes. No olviden crear y ejecutar las migraciones.

- Incluir la gestión de las tablas auxiliares cómo modelos para la administración de Django, de tal
forma que, sólo los superuser puedan gestionarlas.

- RFG-003, desplegará la lista de pedidos registrados, cualquier sea su origen. En esta vista, en la
barra de navegación se deberán considerar las opciones: Gestión de Productos y Logout. 

-En la parte superior de la lista de pedidos, deberá existir un botón que permitirá Tomar un Pedido; en
cada elemento de la lista deberá existir un botón que permita la visualización del pedido.

    RFG-003 - Realizar seguimiento de los pedidos:
    Los usuarios habilitados para ingresar a este módulo, podrán visualizar una 
    lista de todos los pedidos     realizados, así como el estado en el que se 
    encuentra cada uno de estos pedidos (pendiente, en     preparación, en despacho,
    entregado).

    El usuario podrá actualizar el estado de cada pedido en la medida que avanza
    el proceso de entrega.
    
    Eventualmente, el sistema deberá enviar notificaciones a los clientes por correo 
    electrónico por cada cambio de estado del pedido.

----------------
AE3
----------------

- RFG-003, a partir de la acción sobre el registro para visualizar el pedido, se 
desplegará la identificación del cliente, las instrucciones de despacho y los
productos vinculados. Desde aquí el usuario de staff o superuser podrá realizar 
acciones para el cambio de estado del pedido.


    RFG-003 - Realizar seguimiento de los pedidos:
    Los usuarios habilitados para ingresar a este módulo, podrán visualizar una 
    lista de todos los pedidos     realizados, así como el estado en el que se 
    encuentra cada uno de estos pedidos (pendiente, en     preparación, en despacho,
    entregado).

    El usuario podrá actualizar el estado de cada pedido en la medida que avanza
    el proceso de entrega.
    
    Eventualmente, el sistema deberá enviar notificaciones a los clientes por correo 
    electrónico por cada cambio de estado del pedido.

- RFG-001, gestionar los productos que sobre los cuales se realizarán pedidos.

    RFG-001 - Definir productos:
    Los usuarios superuser o staff podrán gestionar los productos que se utilizarán 
    para que los usuarios,internos y externos, puedan realizar los pedidos 
    correspondientes.

    Los atributos de los productos serán definidos por ustedes de acuerdo a los
    trabajos que hayan realizado previamente.

--------------
AE4
--------------

- RFW-001. En el área de login de la página principal, se deberá habilitar un link que llegue al
registro de los usuarios según el requerimiento. Una vez registrado, el usuario deberá ingresar con
sus credenciales según RFW-002.

    RFW-001 - Registro de usuarios:
    Para que los usuarios puedan realizar pedidos, éstos deben estar registrados
    en el sitio. Por tal razón, este requerimiento solicita el registro deL
    usuario en el sitio, proporcionando su correo electrónico, rut y nombre completo.

    Éste deberá ser registrado como un usuario normal según el modelo User de Django,
    el que no podrá acceder al Módulo de Gestión. El sistema verificará la veracidad
    del correo electrónico enviando una contraseña aleatoria de 6 caracteres
    (entre letras y números), con la finalidad de confirmar al usuario.

    Ésta será la contraseña que deberá utilizar el usuario al ingresar a sus pedidos.

- RFG-002, permitirá a los usuarios superuser o staff tomar pedidos y registrarlos en el sistema.

    RFG-002 - Tomar pedidos: Los usuarios habilitados para ingresar a este módulo,
    podrán     tomar     pedidos que provengan de llamadas telefónicas, correo
    electrónico u otro medio digital distinto al sitio web. Aquí deberán ingresar
    los datos del cliente, dirección de entrega, detalle de los productos solicitados 
    (considerando precios y cantidades) y la forma de pago que el cliente utilizará.

    El sistema deberá generar automáticamente un número único para cada pedido.




