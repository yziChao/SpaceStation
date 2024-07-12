import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    crear_usuario(
        username='jperez',
        tipo='Cliente', 
        nombre='Juan', 
        apellido='Perez', 
        correo=test_user_email if test_user_email else 'jperez@jotmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='25.747.200-0',	
        direccion='Tenderini 82 P. 7, Región Metropolitana de Santiago', 
        subscrito=True, 
        imagen='perfiles/jperez.jpg')

    crear_usuario(
        username='jgonzalez',
        tipo='Cliente', 
        nombre='Juana', 
        apellido='Gonzalez', 
        correo=test_user_email if test_user_email else 'jgonzalez@jotmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12.202.357-5', 
        direccion='Calle Isabel Riquelme, 895', 
        subscrito=True, 
        imagen='perfiles/jgonzalez.jpg')

    crear_usuario(
        username='mpinto',
        tipo='Cliente', 
        nombre='Manuel', 
        apellido='Pinto', 
        correo=test_user_email if test_user_email else 'mpinto@jotmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='11.991.600-3', 
        direccion='Avenida 21 De Mayo, 1465', 
        subscrito=False, 
        imagen='perfiles/mpinto.jpg')

    crear_usuario(
        username='nriffo',
        tipo='Cliente', 
        nombre='Natalia', 
        apellido='Riffo', 
        correo=test_user_email if test_user_email else 'nriffo@jotmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='16.469.725-8', 
        direccion='Avenida Valle Del Maipo 4134 barrio Las Rosas, Maipú', 
        subscrito=False, 
        imagen='perfiles/nriffo.jpg')

    crear_usuario(
        username='mgranifo',
        tipo='Administrador', 
        nombre='Marion', 
        apellido='Granifo', 
        correo=test_user_email if test_user_email else 'mari.granifo@duocuc.cl', 
        es_superusuario=False, 
        es_staff=True, 
        rut='19.441.980-5', 
        direccion='García Sierpes 05.', 
        subscrito=False, 
        imagen='perfiles/mgranifo.jpg')
    
    crear_usuario(
        username='triveros',
        tipo='Administrador', 
        nombre='Tomas', 
        apellido='Riveros', 
        correo=test_user_email if test_user_email else 't.riveros@duocuc.cl', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.708.052-5', 
        direccion='Avenida Los Dominicos, 8176 - Of. 8', 
        subscrito=False, 
        imagen='perfiles/triveros.jpg')
    
    crear_usuario(
        username='zyuan',
        tipo='Administrador', 
        nombre='Zichao', 
        apellido='Yuan', 
        correo=test_user_email if test_user_email else 'zi.yuan@duocuc.cl', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21.966.370-6', 
        direccion='Calle Tabare 681 , Recoleta', 
        subscrito=False, 
        imagen='perfiles/ziyuan.jpg')

    crear_usuario(
        username='Spacestation',
        tipo='Superusuario',
        nombre='Space',
        apellido='Station',
        correo=test_user_email if test_user_email else 'SpaceStation@spstt.com',
        es_superusuario=True,
        es_staff=True,
        rut='13.029.317-4',
        direccion='12777 Jefferson Blvd, Los Angeles, CA 90066',
        subscrito=False,
        imagen='perfiles/spst.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Acción" (8 juegos)
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'The Outlast Trials',
            'descripcion': 'Descripción Una vez dentro, su única esperanza de escapar reside en la terrible verdad que se oculta en el corazón del monte Massive. Outlast es toda una experiencia de horror y supervivencia que pretende demostrar que los monstruos más terribles se originan en la mente humana.',
            'precio': 21990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/otlast.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Need For Speed',
            'descripcion': 'Need for Speed es un juego de conducción arcade en mundo abierto desarrollado por Ghost Games y Electronic Arts para PS4, Xbox One y PC. Las carreras ilegales y el tuning vuelven en esta entrega en la que tenemos que competir siempre de noche por las calles de Ventura Bay, conduciendo algunos de los coches más lujosos del mercado.',
            'precio': 12999,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/nfs.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Assetto Corsa',
            'descripcion': 'Assetto Corsa es un simulador de conducción desarrollado y publicado por Kunos Simulazioni para PlayStation 4, Xbox One y PC. Uno de los juegos de coches más realistas del mercado y que satisface a los apasionados del motor más exigentes, con un gameplay exigente y complejo, un sofisticado sistema de físicas y la enorme atención al detalle en el diseño de los coches y los circuitos, recreados de manera realista al ser digitalizados mediante láser.',
            'precio': 30990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/asseto.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Dying Light 2',
            'descripcion': 'Dying Light 2 es un juego de acción y rol en primera persona para PlayStation 4, PlayStation 5, Xbox One, Xbox Series y PC desarrollado por Techland que, como en la primera parte, vuelve a hacer gala de un sistema de parkour y saltos imposibles. Ambientado en un mundo en el que ser el humano sobrevive como puede a la amenaza de los no muertos, esta segunda parte añade mecánicas y sistemas de juego más ambiciosos y complejos.',
            'precio': 17990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/dy2.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Cyber punk 2077',
            'descripcion': 'Cyberpunk 2077 es el nuevo videojuego de rol en primera persona con estructura de mundo abierto de CD Projekt RED. Los padres de The Witcher nos presentan para Xbox One, PC y PS4 una aventura de corte futurista y ciberpunk en la que encarnaremos a un personaje diseñado a nuestra medida y en la que tendremos que sobrevivir en una peligrosa urbe plagada de corporaciones, ciborgs, bandas y las más variadas amenazas tecnológicas.',
            'precio': 36990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/cyber.jpg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Elden Ring',
            'descripcion': 'Elden Ring es un juego de rol de acción desarrollado por FromSoftware y publicado por Bandai Namco Entertainment. El juego se desarrolla en un mundo abierto llamado las Tierras Intermedias, donde los jugadores controlan a un personaje conocido como el Sinluz, que debe viajar por el mundo para restaurar el Elden Ring, un poderoso artefacto que ha sido destruido.',
            'precio': 59990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/elden.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'God of War 4',
            'descripcion': 'God of War es la vuelta de Kratos a los videojuegos tras la trilogía original. Esta nueva entrega para PlayStation 4, si bien mantendrá varios de los ingredientes indivisibles de su jugabilidad, apostará por un nuevo comienzo para el personaje y una ambientación nórdica, ofreciéndonos una perspectiva más madura y realista de la mitología de dioses y monstruos milenarios habitual en la serie de títulos. En God of War, Kratos será un guerrero más curtido y pasivo, pues tendrá que desempeñar el rol de padre en un frío y hostil escenario, al que parece haberse retirado para olvidar su pasado.',
            'precio': 30990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/gow2.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Resident Evil 4',
            'descripcion': 'Resident Evil 4 Remake es la reimaginación del clásico juego de acción y terror en tercera persona desarrollado por Capcom para PlayStation 4 y 5, Xbox One, Xbox Series S y X y PC. Se trata de la puesta al día del survival horror de la saga Resident Evil lanzado en 2005, una ambiciosa puesta al día a nivel jugable y gráfico que nos devuelve a Leon S. Kennedy en su viaje a un récondito pueblo de España en su rescate de la hija del presidente de Estados Unidos.',
            'precio': 38990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/re4.jpg'
        },
        # Categoría "Aventura" (4 juegos)
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Minecraft',
            'descripcion': 'Minecraft es un videojuego tipo sandbox, su traducción literal sería “caja de arena” y es lo que representa la experiencia de juego. Los jugadores pueden modelar el mundo a su gusto, destruir y construir, como si estuviesen jugando en una caja de arena.',
            'precio': 23990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/minecraf.jpg'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Terraria 2',
            'descripcion': 'Terraria 2 es un juego de supervivencia desarrollado por Re-Logic. La secuela del popular y exitoso sandbox en 2D, uno de los indies más exitosos de todos los tiempos, que tiene la tarea de superar un juego completísimo y que sigue siendo de los más jugados más de diez años después de su lanzamiento, que promete ofrecer nuevas mecánicas, gráficos mejorados y mundo infinitos.',
            'precio': 5990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 20,
            'imagen': 'productos/terraria.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Red Dead Redemtion 2',
            'descripcion': 'Red Dead Redemption 2, desarrollado por Rockstar Games, es una épica de acción-aventura en un mundo abierto que representa la cúspide del diseño de videojuegos moderno. Originalmente lanzado para PlayStation 4 y Xbox One en 2018, el juego fue posteriormente adaptado para PC en 2019, brindando mejoras significativas en gráficos y rendimiento, así como contenido adicional.',
            'precio': 23990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/rdr2.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Skyrim',
            'descripcion': 'The Elder Scrolls V: Skyrim es un videojuego de rol de acción de mundo abierto desarrollado por Bethesda Game Studios y publicado por Bethesda Softworks. Es la quinta entrega de la serie de fantasía The Elder Scrolls y es posterior a Oblivion y predecesor de Online.',
            'precio': 30990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/skyrim.jpg'
        },
        # Categoría "Estrategia" (4 juegos)
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Starcraft 2',
            'descripcion': 'StarCraft II es un videojuego de estrategia en tiempo real actualmente en desarrollo por parte de Blizzard Entertainment para PC Windows y Macintosh. Será la segunda parte de StarCraft (1998).',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/sc2.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Age of Empires IV',
            'descripcion': 'Age of Empires IV es un juego de estrategia en tiempo real desarrollado por Relic Entertainment y publicado por Xbox Game Studios. El juego es la cuarta entrega principal de la serie Age of Empires y fue lanzado en octubre de 2021. El juego presenta ocho civilizaciones jugables, cada una con sus propias unidades, tecnologías y edificios únicos.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/age.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Northgard',
            'descripcion': 'Northgard es un juego de estrategia aclamado por la crítica basado en la mitología nórdica. ¡Lidera tu clan, descubre los secretos de un misterioso continente recién descubierto y derrota a tus enemigos para conquistar el trono!',
            'precio': 24990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/northgard.jpg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Magic: The Gathering',
            'descripcion': 'Magic: The Gathering es el juego de cartas intercambiables original, que ahora puedes descargar y al que puedes jugar gratis con amigos desde cualquier parte. Magic: The Gathering Arena te permite descubrir estrategias, conocer a los planeswalkers, explorar el Multiverso y enfrentarte a amigos de todo el mundo.',
            'precio': 5990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/mtg.jpg'
        },
        # Categoría "RPG" (4 juegos)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Hogwarts Legacy',
            'descripcion': 'The Witcher 3: Wild Hunt es un juego de rol de acción de mundo abierto desarrollado y publicado por CD Projekt Red. El juego sigue a Geralt de Rivia, un cazador de monstruos profesional conocido como brujo, mientras busca a su hija adoptiva, Ciri, quien está siendo perseguida por la Cacería Salvaje, una fuerza espectral que busca usar sus poderes para sus propios fines.',
            'precio': 39990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/hogwart.jpg'
        },
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['25.747.200-0', '11.991.600-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

