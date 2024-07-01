from datetime import date
from .zpoblar import poblar_bd
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.utils.safestring import SafeString
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Producto, Boleta, Carrito, DetalleBoleta, Bodega, Perfil
from .forms import ProductoForm, BodegaForm, IngresarForm, UsuarioForm, PerfilForm
from .forms import RegistroUsuarioForm, RegistroPerfilForm
from .templatetags.custom_filters import formatear_dinero, formatear_numero
from .tools import eliminar_registro, verificar_eliminar_registro, show_form_errors
from django.core.mail import send_mail

# *********************************************************************************************************#
#                                                                                                          #
# INSTRUCCIONES PARA EL ALUMNO, PUEDES SEGUIR EL VIDEO TUTORIAL, COMPLETAR EL CODIGO E INCORPORAR EL TUYO: #
#                                                                                                          #
# https://drive.google.com/drive/folders/1ObwMnpKmCXVbq3SMwJKlSRE0PCn0buk8?usp=drive_link                  #
#                                                                                                          #
# *********************************************************************************************************#

# Se usará el decorador "@user_passes_test" para realizar la autorización básica a las páginas.
# De este modo sólo entrarán a las páginas las personas que sean del tipo_usuario permitido.
# Si un usuario no autorizado intenta entrar a la página, será redirigido al inicio o a ingreso

# Revisar si el usuario es personal de la empresa (staff administrador o superusuario) autenticado y con cuenta activa
def es_personal_autenticado_y_activo(user):
    return (user.is_staff or user.is_superuser) and user.is_authenticated and user.is_active

# Revisar si el usuario no está autenticado, es decir, si aún está navegando como usuario anónimo
def es_usuario_anonimo(user):
    return user.is_anonymous

# Revisar si el usuario es un cliente (no es personal de la empresa) autenticado y con cuenta activa
def es_cliente_autenticado_y_activo(user):
    return (not user.is_staff and not user.is_superuser) and user.is_authenticated and user.is_active

def inicio(request):

    if request.method == 'POST':
        # Si la vista fue invocada con un POST es porque el usuario presionó el botón "Buscar" en la página principal.
        # Por lo anterior, se va a recuperar palabra clave del formulario que es el campo "buscar" (id="buscar"), 
        # que se encuentra en la página Base.html. El formulario de búsqueda se encuentra bajo el comentario 
        # "FORMULARIO DE BUSQUEDA" en la página Base.html.
        buscar = request.POST.get('buscar')

        # Se filtrarán todos los productos que contengan la palabra clave en el campo nombre
        registros = Producto.objects.filter(nombre__icontains=buscar).order_by('nombre')
    
    if request.method == 'GET':
        # Si la vista fue invocada con un GET, se devolverán todos los productos a la PAGINA
        registros = Producto.objects.all().order_by('nombre')

    # Como los productos tienen varios cálculos de descuentos por ofertas y subscripción, estos se realizarán
    # en una función a parte llamada "obtener_info_producto", mediante la cuál se devolverán las filas de los
    # productos, pero con campos nuevos donde los cálculos ya han sido realizados.
    productos = []
    for registro in registros:
        productos.append(obtener_info_producto(registro.id))

    context = { 'productos': productos }
    
    return render(request, 'core/inicio.html', context)

def ficha(request, producto_id):
    context = obtener_info_producto(producto_id)
    return render(request, 'core/ficha.html', context)

def nosotros(request):
    return render(request, 'core/nosotros.html')

def premio(request):
    return render(request, 'core/api.html')

@user_passes_test(es_usuario_anonimo, login_url='inicio')
def ingresar(request):
    if request.method == "POST":
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.POST.get('recordar_cuenta'):
                        # Si el checkbox está marcado, establecer la cookie para recordar la sesión
                        request.session.set_expiry(1209600)  # 2 semanas en segundos
                    messages.success(request, f'¡Bienvenido(a) {user.first_name} {user.last_name}!')
                    return redirect(inicio)
                else:
                    messages.error(request, 'La cuenta está desactivada.')
            else:
                messages.error(request, 'La cuenta o la contraseña no son correctos.')
        else:
            messages.error(request, 'No se pudo ingresar al sistema.')
            show_form_errors(request, [form])

    else:  # Método GET
        form = IngresarForm()

    context = {
        'form': form,
        'perfiles': Perfil.objects.all().order_by('tipo_usuario', 'subscrito'),
    }

    return render(request, "core/ingresar.html", context)

@login_required
def salir(request):
    nombre = request.user.first_name
    apellido = request.user.last_name
    messages.success(request, f'¡Hasta pronto {nombre} {apellido}!')
    logout(request)
    return redirect(inicio)

@user_passes_test(es_usuario_anonimo)
def registrarme(request):

    if request.method == 'POST':
        
        form_usuario = RegistroUsuarioForm(request.POST)
        form_perfil = RegistroPerfilForm(request.POST, request.FILES)

        if form_usuario.is_valid() and form_perfil.is_valid():
            usuario = form_usuario.save(commit=False)
            usuario.is_staff = False
            perfil = form_perfil.save(commit=False)
            usuario.save()
            perfil.usuario_id = usuario.id
            perfil.tipo_usuario = 'Cliente'
            perfil.save()
            premium = 'y aprovechar tus descuentos especiales como cliente PREMIUM' if hasattr(perfil, 'premium') and perfil.premium else ''
            mensaje = f'Tu cuenta de usuario: "{usuario.username}" ha sido creada con éxito. ¡Ya puedes iniciar sesión {premium}!'
            messages.success(request, mensaje)
            return redirect(ingresar)
        else:
            messages.error(request, 'No fue posible crear tu cuenta de cliente.')
        show_form_errors(request, [form_usuario, form_perfil])

    if request.method == 'GET':

        form_usuario = RegistroUsuarioForm(request=request)
        form_perfil = RegistroPerfilForm()

    context = {
        'form_usuario': form_usuario,
        'form_perfil': form_perfil,
    }

    return render(request, 'core/registrarme.html', context)


@login_required
def misdatos(request):
    # Obtener el usuario actual y sus datos de perfil
    usuario_actual = request.user
    perfil_usuario_actual = usuario_actual.perfil

    if request.method == 'POST':
        # Si se está enviando el formulario (POST)
        form_usuario = UsuarioForm(request.POST, instance=usuario_actual)
        form_perfil = RegistroPerfilForm(request.POST, request.FILES, instance=perfil_usuario_actual)

        if form_usuario.is_valid() and form_perfil.is_valid():
            usuario_actual = form_usuario.save()
            perfil_actualizado = form_perfil.save(commit=False)
            perfil_actualizado.usuario = usuario_actual
            perfil_actualizado.save()

            # Lógica opcional para definir tipo de cuenta
            if perfil_actualizado.tipo_usuario in ['Administrador', 'Superusuario']:
                tipo_cuenta = perfil_actualizado.tipo_usuario
            else:
                tipo_cuenta = 'CLIENTE PREMIUM' if perfil_actualizado.subscrito else 'cliente'

            messages.success(request, f'Tu cuenta de {tipo_cuenta} ha sido actualizada con éxito.')
            return redirect('misdatos')  # Redirige a la misma página después de guardar

    else:
        # Si es una solicitud GET, mostrar los formularios con los datos actuales
        form_usuario = UsuarioForm(instance=usuario_actual)
        form_perfil = RegistroPerfilForm(instance=perfil_usuario_actual)

    # Contexto para enviar los formularios a la plantilla
    context = {
        'form_usuario': form_usuario,
        'form_perfil': form_perfil,
    }

    return render(request, 'core/misdatos.html', context)

@login_required
def boleta(request, nro_boleta):
    try:
        boleta = Boleta.objects.get(numero=nro_boleta)
        
        detalles = DetalleBoleta.objects.filter(boleta=boleta)
        
        context = {
            'boleta': boleta,
            'detalles': detalles,
        }
        
    except Boleta.DoesNotExist:
        context = {
            'error_message': 'La boleta especificada no existe.'
        }
    
    return render(request, 'core/boleta.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def ventas(request):
    
    # CREAR: lógica para ver las ventas

    # CREAR: variable de contexto para enviar historial de ventas
    context = { }

    return render(request, 'core/ventas.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def productos(request, accion, id=None):
    if request.method == 'POST':
        if accion == 'crear':
            form = ProductoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto creado exitosamente.')
                return redirect('productos', accion='ver', id=0)  # Redirige a la vista de todos los productos
            else:
                messages.error(request, 'Error al crear el producto.')

        elif accion == 'actualizar' and id:
            producto = get_object_or_404(Producto, id=id)
            form = ProductoForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto actualizado exitosamente.')
                return redirect('productos', accion='ver', id=0)  # Redirige a la vista de todos los productos
            else:
                messages.error(request, 'Error al actualizar el producto.')

        elif accion == 'eliminar' and id:
            producto = get_object_or_404(Producto, id=id)
            producto.delete()
            messages.success(request, 'Producto eliminado exitosamente.')
            return redirect('productos', accion='ver', id=0)  # Redirige a la vista de todos los productos

    if request.method == 'GET':
        if accion == 'crear':
            form = ProductoForm()
        elif accion == 'actualizar' and id:
            producto = get_object_or_404(Producto, id=id)
            form = ProductoForm(instance=producto)
        elif accion == 'eliminar' and id:
            producto = get_object_or_404(Producto, id=id)
            form = ProductoForm(instance=producto)  # Para confirmar eliminación
        else:  # Ver todos los productos
            form = None

        productos = Producto.objects.all()
        context = {
            'form': form,
            'productos': productos,
            'accion': accion,
            'id': id,
        }
        return render(request, 'core/productos.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def usuarios(request, accion, id):
    if request.method == 'POST':
        if accion == 'crear':
            form_usuario = UsuarioForm(request.POST)
            form_perfil = PerfilForm(request.POST, request.FILES)

            if form_usuario.is_valid() and form_perfil.is_valid():
                usuario = form_usuario.save(commit=False)
                usuario.is_staff = False  # Asignar el rol adecuado
                usuario.save()

                perfil = form_perfil.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

                return redirect('nombre_de_tu_vista')  # Redirigir a la vista de usuarios

        if accion == 'actualizar':
            usuario = get_object_or_404(User, id=id)
            perfil = get_object_or_404(Perfil, usuario=usuario)

            form_usuario = UsuarioForm(request.POST, instance=usuario)
            form_perfil = PerfilForm(request.POST, request.FILES, instance=perfil)

            if form_usuario.is_valid() and form_perfil.is_valid():
                form_usuario.save()
                form_perfil.save()

                return redirect('nombre_de_tu_vista')  # Redirigir a la vista de usuarios

    if request.method == 'GET':
        if accion == 'eliminar':
            usuario = get_object_or_404(User, id=id)
            usuario.delete()
            return redirect('nombre_de_tu_vista')  # Redirigir a la vista de usuarios

        if accion == 'crear':
            form_usuario = UsuarioForm()
            form_perfil = PerfilForm()
        else:
            usuario = get_object_or_404(User, id=id)
            perfil = get_object_or_404(Perfil, usuario=usuario)
            form_usuario = UsuarioForm(instance=usuario)
            form_perfil = PerfilForm(instance=perfil)

    context = {
        'form_usuario': form_usuario,
        'form_perfil': form_perfil,
        'usuarios': User.objects.all(),  # O tu queryset personalizado
    }

    return render(request, 'core/usuarios.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def bodega(request):

    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            # Guardar el formulario y procesar la información del producto
            producto = form.save(commit=False)
            producto.save()
            messages.success(request, 'Producto agregado correctamente a la bodega.')
            return redirect('bodega')  # Redirige a la misma vista para evitar reenvíos de formulario

    else:
        form = BodegaForm()

    registros = Bodega.objects.all()
    lista = []
    for registro in registros:
        vendido = DetalleBoleta.objects.filter(bodega=registro).exists()
        item = {
            'bodega_id': registro.id,
            'nombre_categoria': registro.producto.categoria.nombre,
            'nombre_producto': registro.producto.nombre,
            'estado': 'Vendido' if vendido else 'En bodega',
            'imagen': registro.producto.imagen,
        }
        lista.append(item)

    context = {
        'form': BodegaForm(),
        'productos': lista,
    }
    
    return render(request, 'core/bodega.html', context)


@user_passes_test(es_personal_autenticado_y_activo)
def obtener_productos(request):
    # La vista obtener_productos la usa la pagina "Administracion de bodega", para
    # filtrar el combobox de productos cuando el usuario selecciona una categoria
    
    # CREAR: Un JSON para devolver los productos que corresponden a la categoria

    data = []
    return JsonResponse(data, safe=False)

@user_passes_test(es_personal_autenticado_y_activo)
def eliminar_producto_en_bodega(request, bodega_id):
    # La vista eliminar_producto_en_bodega la usa la pagina "Administracion de bodega", 
    # para eliminar productos que el usuario decidio sacar del inventario

    # CREAR: lógica para eliminar un producto de la bodega

    return redirect(bodega)

@user_passes_test(es_cliente_autenticado_y_activo)
def miscompras(request):

    # CREAR: lógica para ver las compras del cliente

    # CREAR: variable de contexto para enviar el historial de compras del cliente
    context = { }

    return render(request, 'core/miscompras.html', context)


# ***********************************************************************
# FUNCIONES Y VISTAS AUXILIARES QUE SE ENTREGAN PROGRAMADAS AL ALUMNO
# ***********************************************************************

# VISTA PARA CAMBIAR ESTADO DE LA BOLETA

@user_passes_test(es_personal_autenticado_y_activo)
def cambiar_estado_boleta(request, nro_boleta, estado):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    if estado == 'Anulado':
        # Anular boleta, dejando la fecha de anulación como hoy y limpiando las otras fechas
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    elif estado == 'Vendido':
        # Devolver la boleta al estado recien vendida al dia de hoy, y sin despacho ni entrega
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    elif estado == 'Despachado':
        # Cambiar boleta a estado despachado, se conserva la fecha de venta y se limpia la fecha de entrega
        boleta.fecha_despacho = date.today()
        boleta.fecha_entrega = None
    elif estado == 'Entregado':
        # Cambiar boleta a estado entregado, pero hay que ver que estado actual tiene la boleta
        if boleta.estado == 'Vendido':
            # La boleta esta emitida, pero sin despacho ni entrega, entonces despachamos y entregamos hoy
            boleta.fecha_despacho = date.today()
            boleta.fecha_entrega = date.today()
        elif boleta.estado == 'Despachado':
            # La boleta esta despachada, entonces entregamos hoy
            boleta.fecha_entrega = date.today()
        elif boleta.estado == 'Entregado':
            # La boleta esta entregada, pero si se trata de un error entonces entregamos hoy
            boleta.fecha_entrega = date.today()
    boleta.estado = estado
    boleta.save()
    return redirect(ventas)

# FUNCIONES AUXILIARES PARA OBTENER: INFORMACION DE PRODUCTOS, CALCULOS DE PRECIOS Y OFERTAS

def obtener_info_producto(producto_id):

    # Obtener el producto con el id indicado en "producto_id"
    producto = Producto.objects.get(id=producto_id)

    # Se verificará cuántos productos hay en la bodega que tengan el id indicado en "producto_id".
    # Para lograrlo se filtrarán en primer lugar los productos con el id indicado. Luego, se 
    # realizará un JOIN con la tabla de "DetalleBoleta" que es donde se indican los productos
    # que se han vendido desde la bodega, sin olvidar que los modelos funcionan con Orientación
    # a Objetos, lo que hace que las consultas sean un poco diferentes a las de SQL. 
    # DetalleBoleta está relacionada con la tabla Bodega por medio de su propiedad "bodega",
    # la cual internamente agrega en la tabla DetalleBoleta el campo "bodega_id", que permite
    # que se relacione con la tabla Bodega. Para calcular cuántos productos quedan en la Bodega
    # se debe excluir aquellos que ya fueron vendidos, lo que se logra con la condición
    # "detalleboleta__isnull=False", es decir, se seleccionarán aquellos registros de Bodega
    # cuya relación con la tabla de DetalleBoleta esté en NULL, osea los que no han sido vendidos.
    # Si un producto de la Bodega estuviera vendido, entonces tendría su relación "detalleboleta"
    # con un valor diferente de NULL, ya que el campo "bodega_id" de la tabla DetalleBoleta
    # tendría el valor del id de Bodega del producto que se vendió.
    stock = Bodega.objects.filter(producto_id=producto_id).exclude(detalleboleta__isnull=False).count()
    
    # Preparar texto para mostrar estado: en oferta, sin oferta y agotado
    con_oferta = f'<span class="text-primary"> EN OFERTA {producto.descuento_oferta}% DE DESCUENTO </span>'
    sin_oferta = '<span class="text-success"> DISPONIBLE EN BODEGA </span>'
    agotado = '<span class="text-danger"> AGOTADO </span>'

    if stock == 0:
        estado = agotado
    else:
        estado = sin_oferta if producto.descuento_oferta == 0 else con_oferta

    # Preparar texto para indicar cantidad de productos en stock
    en_stock = f'En stock: {formatear_numero(stock)} {"unidad" if stock == 1 else "unidades"}'
   
    return {
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'imagen': producto.imagen,
        'html_estado': estado,
        'html_precio': obtener_html_precios_producto(producto),
        'html_stock': en_stock,
    }

def obtener_html_precios_producto(producto):
    
    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(producto)
    
    normal = f'Precio: {formatear_dinero(precio_normal)}'
    tachar = f'Precio: <span class="text-decoration-line-through"> {formatear_dinero(precio_normal)} </span>'
    oferta = f'Oferta: <span class="text-success"> {formatear_dinero(precio_oferta)} </span>'
    subscr = f'Subscrito: <span class="text-danger"> {formatear_dinero(precio_subscr)} </span>'

    if hay_desc_oferta > 0:
        texto_precio = f'{tachar}<br>{oferta}'
    else:
        texto_precio = normal

    if hay_desc_subscr > 0:
        texto_precio += f'<br>{subscr}'

    return texto_precio

def calcular_precios_producto(producto):
    precio_normal = producto.precio
    precio_oferta = producto.precio * (100 - producto.descuento_oferta) / 100
    precio_subscr = producto.precio * (100 - (producto.descuento_oferta + producto.descuento_subscriptor)) / 100
    hay_desc_oferta = producto.descuento_oferta > 0
    hay_desc_subscr = producto.descuento_subscriptor > 0
    return precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr

# VISTAS y FUNCIONES DE COMPRAS

def comprar_ahora(request):
    messages.error(request, f'El pago aún no ha sido implementado.')
    return redirect(inicio)

@user_passes_test(es_cliente_autenticado_y_activo)
def carrito(request):

    detalle_carrito = Carrito.objects.filter(cliente=request.user.perfil)

    total_a_pagar = 0
    for item in detalle_carrito:
        total_a_pagar += item.precio_a_pagar
    monto_sin_iva = int(round(total_a_pagar / 1.19))
    iva = total_a_pagar - monto_sin_iva

    context = {
        'detalle_carrito': detalle_carrito,
        'monto_sin_iva': monto_sin_iva,
        'iva': iva,
        'total_a_pagar': total_a_pagar,
    }

    return render(request, 'core/carrito.html', context)

def agregar_producto_al_carrito(request, producto_id):

    if es_personal_autenticado_y_activo(request.user):
        messages.error(request, f'Para poder comprar debes tener cuenta de Cliente, pero tu cuenta es de {request.user.perfil.tipo_usuario}.')
        return redirect(inicio)
    elif es_usuario_anonimo(request.user):
        messages.info(request, 'Para poder comprar, primero debes registrarte como cliente.')
        return redirect(registrarme)

    perfil = request.user.perfil
    producto = Producto.objects.get(id=producto_id)

    precio_normal, precio_oferta, precio_subscr, hay_desc_oferta, hay_desc_subscr = calcular_precios_producto(producto)

    precio = producto.precio
    descuento_subscriptor = producto.descuento_subscriptor if perfil.subscrito else 0
    descuento_total=producto.descuento_subscriptor + producto.descuento_oferta if perfil.subscrito else producto.descuento_oferta
    precio_a_pagar = precio_subscr if perfil.subscrito else precio_oferta
    descuentos = precio - precio_subscr if perfil.subscrito else precio - precio_oferta

    Carrito.objects.create(
        cliente=perfil,
        producto=producto,
        precio=precio,
        descuento_subscriptor=descuento_subscriptor,
        descuento_oferta=producto.descuento_oferta,
        descuento_total=descuento_total,
        descuentos=descuentos,
        precio_a_pagar=precio_a_pagar
    )

    return redirect(ficha, producto_id)

@user_passes_test(es_cliente_autenticado_y_activo)
def eliminar_producto_en_carrito(request, carrito_id):
    Carrito.objects.get(id=carrito_id).delete()
    return redirect(carrito)

@user_passes_test(es_cliente_autenticado_y_activo)
def vaciar_carrito(request):
    productos_carrito = Carrito.objects.filter(cliente=request.user.perfil)
    if productos_carrito.exists():
        productos_carrito.delete()
        messages.info(request, 'Se ha cancelado la compra, el carrito se encuentra vacío.')
    return redirect(carrito)

# CAMBIO DE PASSWORD Y ENVIO DE PASSWORD PROVISORIA POR CORREO

@login_required
def mipassword(request):

    if request.method == 'POST':

        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito, ingresa de nuevo con tu nueva contraseña.')
            return redirect(ingresar)
        else:
            messages.error(request, 'Tu contraseña no pudo ser actualizada.')
            show_form_errors(request, [form])
    
    if request.method == 'GET':

        form = PasswordChangeForm(user=request.user)

    context = {
        'form': form
    }

    return render(request, 'core/mipassword.html', context)

@user_passes_test(es_personal_autenticado_y_activo)
def cambiar_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        existe = User.objects.filter(username=username).exists()
        if existe:
            user = User.objects.get(username=username)
            if user is not None:
                if user.is_active:
                    password = User.objects.make_random_password()
                    user.set_password(password)
                    user.save()
                    enviado = enviar_correo_cambio_password(request, user, password)
                    if enviado:
                        messages.success(request, f'Una nueva contraseña fue enviada al usuario {user.first_name} {user.last_name}')
                    else:
                        messages.error(request, f'No fue posible enviar la contraseña al usuario {user.first_name} {user.last_name}, intente nuevamente más tarde')
                else:
                    messages.error(request, 'La cuenta está desactivada.')
            else:
                messages.error(request, 'La cuenta o la password no son correctos')
        else:
            messages.error(request, 'El usuario al que quiere generar una nueva contraseña ya no existe en el sistema')
    return redirect(usuarios, 'crear', '0')

def enviar_correo_cambio_password(request, user, password):
    try:
        # Revisar "CONFIGURACIÓN PARA ENVIAR CORREOS ELECTRÓNICOS A TRAVÉS DEL SERVIDOR DE GMAIL" en settings.py 
        subject = 'Cambio de contraseña Sword Games Shop'
        url_ingresar = request.build_absolute_uri(reverse(ingresar))
        message = render(request, 'common/formato_correo.html', {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_password': password,
            'link_to_login': url_ingresar,
        })
        from_email = 'info@faithfulpet.com'  # La dirección de correo que aparecerá como remitente
        recipient_list = []
        recipient_list.append(user.email)
        # Enviar el correo
        send_mail(subject=subject, message='', from_email=from_email, recipient_list=recipient_list
            , html_message=message.content.decode('utf-8'))
        return True
    except:
        return False

# POBLAR BASE DE DATOS CON REGISTROS DE PRUEBA

def poblar(request):
    # Permite poblar la base de datos con valores de prueba en todas sus tablas.
    # Opcionalmente se le puede enviar un correo único, para que los Administradores
    # del sistema puedan probar el cambio de password de los usuarios, en la página
    # de "Adminstración de usuarios".
    poblar_bd('zi.yuan@duocuc.cl')
    return redirect(inicio)

