import os
from datetime import datetime
from functools import wraps
from io import BytesIO
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, send_file, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from jinja2 import TemplateNotFound
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from werkzeug.security import check_password_hash, generate_password_hash

from Conexion.conexion import MySQLManager
from forms.producto_form import ProductoForm
from inventario.bd import db
from inventario.persistencia import read_csv, read_json, read_txt, save_csv, save_json, save_txt
from inventario.productos import Producto as ProductoORM
from models.conexion import ConexionSQLite
from models.user import UsuarioLogin
from services.producto_service import ProductoService

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env', override=True)

app = Flask(__name__)

BUSINESS_NAME = 'COMEDOR ALEXANDRA'
BUSINESS_CITY = ''
BUSINESS_HOURS = 'Viernes, Sabado, Domingo y feriados: 2:00 PM a 5:00 AM'
BUSINESS_LOGO = 'logo-comedor-alexandra.svg'
BUSINESS_BANK = 'Banco Pichincha'
BUSINESS_ACCOUNT_TYPE = 'Ahorro'
BUSINESS_ACCOUNT_NUMBER = '2208978980'
BUSINESS_ACCOUNT_OWNER = 'Alexandra Pianda'
BUSINESS_RECEIPT_PHONE = '0992884043'
BUSINESS_HR_EMAIL = 'saidreyes567@gmail.com'
OWNER_EMAIL = os.getenv('OWNER_EMAIL', BUSINESS_HR_EMAIL).strip().lower()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_inventario_2026'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debes iniciar sesion para acceder a esta seccion.'
login_manager.login_message_category = 'error'

db.init_app(app)
db_conexion = ConexionSQLite()
mysql_manager = MySQLManager()
producto_service = ProductoService(mysql_manager)


def is_owner_user(user=None):
    user = user or current_user
    if not getattr(user, 'is_authenticated', False):
        return False
    return (getattr(user, 'email', '') or '').strip().lower() == OWNER_EMAIL


def owner_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not is_owner_user():
            flash('Solo el titular puede acceder a esta seccion.', 'error')
            return redirect(url_for('index'))
        return view_func(*args, **kwargs)

    return wrapper


def normalize_reserva_datetime(raw_value):
    value = (raw_value or '').strip()
    if not value:
        raise ValueError('Debes ingresar la fecha y hora de la reserva.')

    parsed = None
    for fmt in ('%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'):
        try:
            parsed = datetime.strptime(value, fmt)
            break
        except ValueError:
            continue

    if parsed is None:
        raise ValueError('La fecha no tiene un formato valido. Usa fecha y hora reales.')

    if parsed.year < 2000 or parsed.year > 2100:
        raise ValueError('El anio de la reserva no es valido. Verifica la fecha ingresada.')

    return parsed.strftime('%Y-%m-%d %H:%M:%S')


def normalize_cliente_nombre(nombre='', email='', telefono=''):
    base = (nombre or '').strip()
    if base:
        return base

    correo = (email or '').strip().lower()
    if correo and '@' in correo:
        alias = correo.split('@', 1)[0].replace('.', ' ').replace('_', ' ').strip()
        if alias:
            return alias.title()

    tel = ''.join(ch for ch in (telefono or '') if ch.isdigit())
    if tel:
        return f'Cliente {tel[-4:]}'

    return 'Cliente sin nombre'


@login_manager.user_loader
def load_user(user_id):
    try:
        usuario_db = mysql_manager.get_usuario_by_id(user_id)
    except Exception:
        return None
    return UsuarioLogin.from_mysql_row(usuario_db) if usuario_db else None


@app.context_processor
def inject_business_data():
    return {
        'negocio_name': BUSINESS_NAME,
        'negocio_city': BUSINESS_CITY,
        'negocio_hours': BUSINESS_HOURS,
        'negocio_logo': BUSINESS_LOGO,
        'negocio_bank': BUSINESS_BANK,
        'negocio_account_type': BUSINESS_ACCOUNT_TYPE,
        'negocio_account_number': BUSINESS_ACCOUNT_NUMBER,
        'negocio_account_owner': BUSINESS_ACCOUNT_OWNER,
        'negocio_receipt_phone': BUSINESS_RECEIPT_PHONE,
        'negocio_hr_email': BUSINESS_HR_EMAIL,
        'has_auth_routes': True,
        'has_mysql_panel': is_owner_user(),
        'owner_email': OWNER_EMAIL,
    }


with app.app_context():
    db.create_all()

    # Mantiene en Render solo los platos solicitados (y la bebida base) sin agregar platos extra.
    menu_base = [
        (
            'Aguado',
            25,
            3.50,
            'Caldos',
            'Aguado de pollo.',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Chicken_soup.jpg/640px-Chicken_soup.jpg',
        ),
        (
            'Caldo de Pata',
            20,
            3.50,
            'Caldos',
            'Caldo de pata casero.',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Beef_bone_broth.jpg/640px-Beef_bone_broth.jpg',
        ),
        (
            'Carne Asada',
            20,
            4.00,
            'Asados',
            'Carne asada al punto.',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Carne_asada.jpg/640px-Carne_asada.jpg',
        ),
        (
            'Chuleta Asada',
            20,
            4.00,
            'Asados',
            'Chuleta asada a la parrilla.',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Grilled_pork_chop.jpg/640px-Grilled_pork_chop.jpg',
        ),
        (
            'Pollo Asado',
            20,
            4.00,
            'Asados',
            'Pollo asado al carbon.',
            'https://img.freepik.com/fotos-premium/pollo-asado-arroz-plato-primer-plano_848191-330.jpg?w=2000',
        ),
        (
            'Pollo al Jugo',
            20,
            4.00,
            'Tradicional',
            'Pollo al jugo con salsa casera.',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Cooked_chicken.jpg/640px-Cooked_chicken.jpg',
        ),
        (
            'Caldo de Gallina',
            20,
            3.50,
            'Caldos',
            'Caldo de gallina tradicional.',
            'https://tse3.mm.bing.net/th/id/OIP.scKWVE-svuaRalRWQE0U_wHaEN?rs=1&pid=ImgDetMain&o=7&rm=3',
        ),
        (
            'Guatita',
            20,
            4.00,
            'Tradicional',
            'Guatita tradicional.',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Guatita.jpg/640px-Guatita.jpg',
        ),
        (
            'Lengua Guisada',
            20,
            4.00,
            'Tradicional',
            'Lengua guisada en salsa.',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Beef_tongue_stew.jpg/640px-Beef_tongue_stew.jpg',
        ),
        (
            'Seco de Gallina',
            20,
            4.00,
            'Tradicional',
            'Seco de gallina con arroz.',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Seco_de_pollo.jpg/640px-Seco_de_pollo.jpg',
        ),
        (
            'Seco de Carne',
            20,
            4.00,
            'Tradicional',
            'Seco de carne con arroz.',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Beef_stew.jpg/640px-Beef_stew.jpg',
        ),
        (
            'Gaseosa',
            30,
            0.50,
            'Bebidas',
            'Gaseosa personal fria.',
            'https://source.unsplash.com/1200x900/?cola,soft-drink',
        ),
    ]

    existentes = {((p.get('nombre') or '').strip().lower()): p for p in db_conexion.obtener_todos_productos()}
    for nombre, cantidad, precio, categoria, descripcion, imagen in menu_base:
        key = nombre.strip().lower()
        row = existentes.get(key)
        if row:
            db_conexion.actualizar_producto(
                row.get('id'),
                nombre=nombre,
                cantidad=cantidad,
                precio=precio,
                categoria=categoria,
                descripcion=descripcion,
                imagen=imagen,
            )
        else:
            db_conexion.añadir_producto(nombre, cantidad, precio, categoria, descripcion, imagen)

    try:
        mysql_manager.crear_tablas()
        mysql_manager.sync_menu_productos(db_conexion.obtener_todos_productos())
    except Exception as exc:
        print(f"Aviso: no se pudo sincronizar menu inicial con MySQL: {exc}")


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('inicio_acceso.html', negocio_name=BUSINESS_NAME)

    productos = db_conexion.obtener_todos_productos()
    total_productos = len(productos)
    valor_total = db_conexion.obtener_valor_total_inventario()
    bajo_stock = db_conexion.obtener_bajo_stock(5)
    return render_template(
        'index.html',
        total=total_productos,
        valor=valor_total,
        bajo_stock=bajo_stock,
        negocio_name=BUSINESS_NAME,
    )


@app.route('/about')
def about():
    return render_template('about.html', negocio_name=BUSINESS_NAME)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        if not all([nombre, email, password]):
            flash('Completa nombre, email y contrasena.', 'error')
            return redirect(url_for('registro'))

        if len(password) < 6:
            flash('La contrasena debe tener al menos 6 caracteres.', 'error')
            return redirect(url_for('registro'))

        try:
            mysql_manager.insert_usuario(nombre, email, generate_password_hash(password))
            flash('Usuario registrado correctamente. Ahora inicia sesion.', 'success')
            return redirect(url_for('login'))
        except Exception as exc:
            error_text = str(exc).lower()
            if 'duplicate' in error_text or 'unique' in error_text:
                flash('Ese email ya existe en el sistema.', 'error')
            else:
                flash(f'No se pudo registrar el usuario: {exc}', 'error')

    return render_template('registro.html', negocio_name=BUSINESS_NAME)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        if not all([email, password]):
            flash('Ingresa email y contrasena.', 'error')
            return redirect(url_for('login'))

        try:
            usuario_db = mysql_manager.get_usuario_by_email(email)
        except Exception as exc:
            flash(f'Error de conexion con MySQL: {exc}', 'error')
            return redirect(url_for('login'))

        if not usuario_db or not check_password_hash(usuario_db.get('password', ''), password):
            flash('Credenciales invalidas.', 'error')
            return redirect(url_for('login'))

        login_user(UsuarioLogin.from_mysql_row(usuario_db))
        flash('Sesion iniciada correctamente.', 'success')
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', negocio_name=BUSINESS_NAME)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesion cerrada correctamente.', 'success')
    return redirect(url_for('login'))


@app.route('/trabaja-con-nosotros', methods=['GET', 'POST'])
@login_required
def trabaja_con_nosotros():
    if request.method == 'POST':
        nombre_completo = request.form.get('nombre_completo', '').strip()
        nombre_usuario = request.form.get('nombre_usuario', '').strip()
        correo = request.form.get('correo', '').strip().lower()
        telefono = request.form.get('telefono', '').strip()
        cargo_interes = request.form.get('cargo_interes', '').strip()
        password = request.form.get('password', '').strip()

        if not all([nombre_completo, nombre_usuario, correo, password]):
            flash('Completa los campos obligatorios para crear tu usuario.', 'error')
            return redirect(url_for('trabaja_con_nosotros'))

        if len(password) < 6:
            flash('La contrasena debe tener minimo 6 caracteres.', 'error')
            return redirect(url_for('trabaja_con_nosotros'))

        try:
            mysql_manager.insert_usuario_trabajo(
                nombre_completo,
                nombre_usuario,
                correo,
                telefono,
                generate_password_hash(password),
                cargo_interes,
            )
            flash('Usuario creado correctamente. Ahora envia tu hoja de vida al correo indicado.', 'success')
            return redirect(url_for('trabaja_con_nosotros', creado='1'))
        except Exception as exc:
            error_text = str(exc).lower()
            if 'duplicate' in error_text or 'unique' in error_text:
                flash('El nombre de usuario o correo ya existe. Intenta con otro.', 'error')
            else:
                flash(f'No se pudo registrar: {exc}', 'error')

    usuarios = mysql_manager.get_usuarios_trabajo(12)
    creado = request.args.get('creado', '0') == '1'
    return render_template('trabaja.html', usuarios=usuarios, creado=creado, negocio_name=BUSINESS_NAME)


@app.route('/menu')
@app.route('/productos')
@login_required
def productos():
    productos_lista = db_conexion.obtener_todos_productos()
    bebidas = [p for p in productos_lista if (p.get('categoria') or '').strip().lower() == 'bebidas']
    platos = [p for p in productos_lista if (p.get('categoria') or '').strip().lower() != 'bebidas']
    return render_template(
        'productos.html',
        productos=productos_lista,
        platos=platos,
        bebidas=bebidas,
        negocio_name=BUSINESS_NAME,
    )


@app.route('/carrito')
@login_required
def carrito():
    return render_template('carrito.html', negocio_name=BUSINESS_NAME)


@app.route('/pedido/enviar', methods=['POST'])
@login_required
def enviar_pedido():
    payload = request.get_json(silent=True) or {}
    raw_items = payload.get('items') or []
    metodo_pago = str(payload.get('metodo_pago') or 'Efectivo').strip()
    datos_pago = payload.get('datos_pago') or {}
    metodos_validos = {'Efectivo', 'Transferencia', 'Tarjeta', 'Deuna'}

    if not raw_items:
        return jsonify({'ok': False, 'message': 'El carrito esta vacio.'}), 400

    if metodo_pago not in metodos_validos:
        return jsonify({'ok': False, 'message': 'Selecciona un metodo de pago valido.'}), 400

    if not isinstance(datos_pago, dict):
        return jsonify({'ok': False, 'message': 'Los datos de pago son invalidos.'}), 400

    detalle_pago = {}
    if metodo_pago == 'Efectivo':
        monto_entrega = str(datos_pago.get('monto_entrega') or '').strip()
        if not monto_entrega:
            return jsonify({'ok': False, 'message': 'Ingresa el monto con el que vas a pagar.'}), 400
        detalle_pago = {'monto_entrega': monto_entrega}
    elif metodo_pago == 'Transferencia':
        banco = str(datos_pago.get('banco') or '').strip()
        referencia = str(datos_pago.get('referencia') or '').strip()
        if not banco or not referencia:
            return jsonify({'ok': False, 'message': 'Completa banco y numero de referencia para la transferencia.'}), 400
        detalle_pago = {'banco': banco, 'referencia': referencia}
    elif metodo_pago == 'Tarjeta':
        titular = str(datos_pago.get('titular') or '').strip()
        ultimos_digitos = str(datos_pago.get('ultimos_digitos') or '').strip()
        if not titular or len(ultimos_digitos) != 4 or not ultimos_digitos.isdigit():
            return jsonify({'ok': False, 'message': 'Ingresa el titular y los ultimos 4 digitos de la tarjeta.'}), 400
        detalle_pago = {'titular': titular, 'ultimos_digitos': ultimos_digitos}
    elif metodo_pago == 'Deuna':
        telefono = str(datos_pago.get('telefono') or '').strip()
        if len(telefono) < 8:
            return jsonify({'ok': False, 'message': 'Ingresa el telefono asociado a Deuna.'}), 400
        detalle_pago = {'telefono': telefono}

    mysql_manager.crear_tablas()

    items_pedido = []
    for raw_item in raw_items:
        try:
            producto_id = int(raw_item.get('id'))
            cantidad = int(raw_item.get('cantidad', 0))
        except (TypeError, ValueError):
            return jsonify({'ok': False, 'message': 'Hay productos invalidos en el carrito.'}), 400

        if cantidad <= 0:
            return jsonify({'ok': False, 'message': 'La cantidad debe ser mayor a cero.'}), 400

        producto = db_conexion.obtener_producto(producto_id)
        if not producto:
            return jsonify({'ok': False, 'message': f'El producto con ID {producto_id} ya no existe.'}), 404

        id_producto_mysql = mysql_manager.ensure_producto_mysql(
            producto.get('nombre', ''),
            producto.get('categoria', ''),
            int(producto.get('cantidad') or 0),
            float(producto.get('precio') or 0),
        )

        items_pedido.append(
            {
                'id_producto': id_producto_mysql,
                'cantidad': cantidad,
                'precio': float(producto.get('precio') or 0),
                'nombre': producto.get('nombre', ''),
            }
        )

    try:
        factura = mysql_manager.crear_pedido(current_user, items_pedido, metodo_pago, detalle_pago)
    except Exception as exc:
        return jsonify({'ok': False, 'message': f'No se pudo guardar el pedido en MySQL: {exc}'}), 500

    return jsonify(
        {
            'ok': True,
            'message': 'Pedido enviado correctamente a HeidiSQL.',
            'factura': factura,
        }
    )


@app.route('/plato/<string:nombre>')
@login_required
def detalle_plato(nombre):
    producto = next((p for p in db_conexion.obtener_todos_productos() if p.get('nombre') == nombre), None)
    return render_template('plato.html', plato=producto, nombre=nombre, negocio_name=BUSINESS_NAME)


@app.route('/producto/<int:id>')
@login_required
def producto_detalle(id):
    producto = db_conexion.obtener_producto(id)
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos'))
    return render_template('producto_detalle.html', producto=producto, negocio_name=BUSINESS_NAME)


@app.route('/buscar')
@login_required
def buscar():
    termino = request.args.get('termino', '').strip()
    resultados = db_conexion.buscar_producto(termino) if termino else []
    return render_template('buscar.html', termino=termino, resultados=resultados, negocio_name=BUSINESS_NAME)


@app.route('/reserva', defaults={'cliente': ''})
@app.route('/reserva/<cliente>')
@login_required
def reserva(cliente):
    cliente_reserva = (cliente or getattr(current_user, 'nombre', '') or '').strip()
    email_reserva = (getattr(current_user, 'email', '') or '').strip().lower()
    return render_template('reserva.html', cliente=cliente_reserva, email=email_reserva, negocio_name=BUSINESS_NAME)


@app.route('/reserva/confirmar', methods=['POST'])
@login_required
def confirmar_reserva():
    nombre_form = (request.form.get('cliente') or '').strip()
    nombre_usuario = (getattr(current_user, 'nombre', '') or '').strip()
    nombre = (nombre_usuario or nombre_form).strip()
    personas = (request.form.get('personas') or '').strip()
    fecha = (request.form.get('fecha_reserva') or '').strip()
    telefono = (request.form.get('telefono') or '').strip()
    email_usuario = (getattr(current_user, 'email', '') or '').strip().lower()
    email_form = (request.form.get('email') or '').strip().lower()
    email = email_usuario or email_form
    nombre = normalize_cliente_nombre(nombre, email, telefono)

    if not all([nombre, personas, fecha, telefono, email]):
        flash('Completa todos los datos de la reserva.', 'error')
        return redirect(url_for('reserva', cliente=nombre))

    try:
        fecha_mysql = normalize_reserva_datetime(fecha)
    except ValueError as exc:
        flash(str(exc), 'error')
        return redirect(url_for('reserva', cliente=nombre))

    save_json(
        {
            'tipo': 'RESERVA',
            'cliente': nombre,
            'personas': personas,
            'fecha': fecha_mysql,
            'contacto': telefono,
            'email': email,
        }
    )

    try:
        mysql_manager.crear_tablas()
        mysql_manager.insert_reserva(nombre, telefono, email, int(personas), fecha_mysql)
    except Exception as exc:
        flash(f'La reserva se guardo localmente, pero no se pudo enviar a MySQL: {exc}', 'error')
        return render_template('reserva.html', cliente=nombre, email=email, negocio_name=BUSINESS_NAME)

    mensaje_exito = f'Gracias por tu reserva, {nombre}. Tu reserva para {personas} personas el dia {fecha_mysql} ha sido confirmada correctamente y enviada a HeidiSQL.'
    return render_template('reserva.html', cliente=nombre, email=email, mensaje=mensaje_exito, negocio_name=BUSINESS_NAME)


@app.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cantidad = int(request.form.get('cantidad', 0))
        precio = float(request.form.get('precio', 0))
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')
        imagen = request.form.get('imagen')

        id_nuevo = db_conexion.añadir_producto(nombre, cantidad, precio, categoria, descripcion, imagen)
        if id_nuevo > 0:
            record = {'id': id_nuevo, 'nombre': nombre, 'cantidad': cantidad, 'precio': precio}
            save_txt(record)
            save_json(record)
            save_csv(record)
            flash(f'Plato "{nombre}" anadido exitosamente.', 'success')
            return redirect(url_for('productos'))

    return render_template('producto_form.html', negocio_name=BUSINESS_NAME)


@app.route('/producto/anadir-menu/<int:id>', methods=['GET', 'POST'])
@login_required
def anadir_plato_menu(id):
    producto = db_conexion.obtener_producto(id)
    if not producto:
        flash('No se encontro el plato para anadir al menu.', 'error')
        return redirect(url_for('productos'))

    incremento_raw = request.values.get('sumar', '1')
    try:
        incremento = int(incremento_raw)
    except (TypeError, ValueError):
        incremento = 1
    incremento = max(1, min(incremento, 100))

    cantidad_actual = int(producto.get('cantidad') or 0)
    nueva_cantidad = cantidad_actual + incremento
    actualizado = db_conexion.actualizar_producto(id, cantidad=nueva_cantidad)

    if actualizado:
        record = {
            'id': producto.get('id'),
            'nombre': producto.get('nombre'),
            'cantidad': nueva_cantidad,
            'precio': float(producto.get('precio') or 0),
        }
        save_txt(record)
        save_json(record)
        save_csv(record)
        flash(f'Se sumaron {incremento} unidades a {producto.get("nombre")}.', 'success')
    else:
        flash('No se pudo actualizar la cantidad del plato.', 'error')

    return redirect(url_for('productos'))


@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = db_conexion.obtener_producto(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cantidad = int(request.form.get('cantidad', 0))
        precio = float(request.form.get('precio', 0))
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')
        imagen = request.form.get('imagen')

        if db_conexion.actualizar_producto(id, nombre, cantidad, precio, categoria, descripcion, imagen):
            flash('Plato actualizado exitosamente.', 'success')
            return redirect(url_for('productos'))

    return render_template('producto_form.html', producto=producto, es_edicion=True, negocio_name=BUSINESS_NAME)


@app.route('/producto/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    if db_conexion.eliminar_producto(id):
        flash('Plato eliminado.', 'success')
    return redirect(url_for('productos'))


@app.route('/reportes')
@login_required
def reportes():
    productos_lista = db_conexion.obtener_todos_productos()
    valor_total = db_conexion.obtener_valor_total_inventario()
    cantidad_total = sum((p.get('cantidad') or 0) for p in productos_lista)
    bajo_stock = db_conexion.obtener_bajo_stock(5)
    return render_template(
        'reportes.html',
        total_productos=len(productos_lista),
        cantidad_total=cantidad_total,
        valor_total=valor_total,
        bajo_stock=bajo_stock,
        productos=productos_lista,
        negocio_name=BUSINESS_NAME,
    )


@app.route('/mysql/productos-crud')
@login_required
@owner_required
def mysql_productos_lista():
    try:
        resumen = producto_service.resumen()
    except Exception as exc:
        flash(f'No se pudieron cargar productos MySQL: {exc}', 'error')
        resumen = {'productos': [], 'total_items': 0, 'total_stock': 0, 'total_valor': 0}

    return render_template(
        'productos_mysql/lista.html',
        productos=resumen['productos'],
        total_items=resumen['total_items'],
        total_stock=resumen['total_stock'],
        total_valor=float(resumen['total_valor']),
        negocio_name=BUSINESS_NAME,
    )


@app.route('/mysql/productos-crud/nuevo', methods=['GET', 'POST'])
@login_required
@owner_required
def mysql_producto_nuevo():
    form_data = {'nombre': '', 'categoria': '', 'cantidad': 0, 'precio': 0}
    if request.method == 'POST':
        form = ProductoForm(request.form)
        form_data = request.form
        if form.validate():
            data = form.cleaned_data()
            try:
                producto_service.crear(data['nombre'], data['categoria'], data['cantidad'], data['precio'])
                flash('Producto MySQL creado correctamente.', 'success')
                return redirect(url_for('mysql_productos_lista'))
            except Exception as exc:
                flash(f'No se pudo crear el producto: {exc}', 'error')
        else:
            for error in form.errors:
                flash(error, 'error')
    return render_template('productos_mysql/form.html', modo='crear', producto=form_data, negocio_name=BUSINESS_NAME)


@app.route('/mysql/productos-crud/editar/<int:id_producto>', methods=['GET', 'POST'])
@login_required
@owner_required
def mysql_producto_editar(id_producto):
    producto = producto_service.obtener(id_producto)
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('mysql_productos_lista'))

    if request.method == 'POST':
        form = ProductoForm(request.form)
        if form.validate():
            data = form.cleaned_data()
            try:
                producto_service.actualizar(id_producto, data['nombre'], data['categoria'], data['cantidad'], data['precio'])
                flash('Producto MySQL actualizado correctamente.', 'success')
                return redirect(url_for('mysql_productos_lista'))
            except Exception as exc:
                flash(f'No se pudo actualizar: {exc}', 'error')
        else:
            for error in form.errors:
                flash(error, 'error')
        return render_template('productos_mysql/form.html', modo='editar', producto=request.form, id_producto=id_producto, negocio_name=BUSINESS_NAME)

    return render_template('productos_mysql/form.html', modo='editar', producto=producto, id_producto=id_producto, negocio_name=BUSINESS_NAME)


@app.route('/mysql/productos-crud/eliminar/<int:id_producto>', methods=['GET', 'POST'])
@login_required
@owner_required
def mysql_producto_eliminar(id_producto):
    producto = producto_service.obtener(id_producto)
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('mysql_productos_lista'))

    if request.method == 'POST':
        try:
            producto_service.eliminar(id_producto)
            flash('Producto eliminado correctamente.', 'success')
        except Exception as exc:
            flash(f'No se pudo eliminar: {exc}', 'error')
        return redirect(url_for('mysql_productos_lista'))

    return render_template('productos_mysql/eliminar.html', producto=producto, negocio_name=BUSINESS_NAME)


@app.route('/mysql/productos-crud/reporte-pdf')
@login_required
@owner_required
def mysql_productos_reporte_pdf():
    resumen = producto_service.resumen()
    productos_mysql = resumen['productos']
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawString(40, y, 'Reporte de Productos MySQL')
    y -= 18
    pdf.setFont('Helvetica', 10)
    pdf.drawString(40, y, f'Fecha de emision: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    y -= 16
    pdf.drawString(40, y, f'Total items: {resumen["total_items"]} | Stock total: {resumen["total_stock"]} | Valor total: ${float(resumen["total_valor"]):.2f}')
    y -= 24

    pdf.setFont('Helvetica', 9)
    for producto in productos_mysql:
        if y < 60:
            pdf.showPage()
            y = height - 50
        pdf.drawString(40, y, str(producto.id_producto))
        pdf.drawString(80, y, producto.nombre[:30])
        pdf.drawString(260, y, producto.categoria[:15] if producto.categoria else '-')
        pdf.drawRightString(400, y, str(producto.cantidad))
        pdf.drawRightString(500, y, f'${float(producto.precio):.2f}')
        y -= 14

    pdf.save()
    buffer.seek(0)
    return send_file(buffer, mimetype='application/pdf', as_attachment=True, download_name='reporte_productos_mysql.pdf')


@app.route('/datos')
@login_required
def listar_datos():
    return render_template(
        'datos.html',
        txt=read_txt(),
        json_data=read_json(),
        csv=read_csv(),
        db_items=ProductoORM.query.all(),
        negocio_name=BUSINESS_NAME,
    )


@app.route('/mysql/panel')
@login_required
@owner_required
def mysql_panel():
    ok, mensaje = mysql_manager.ping()
    usuarios = []
    productos_mysql = []
    reservas_mysql = []

    if ok:
        try:
            usuarios = mysql_manager.fetch_all('usuarios', 'id_usuario')
            productos_mysql = mysql_manager.fetch_all('productos_mysql', 'id_producto')
            reservas_mysql = mysql_manager.fetch_all('reservas_mysql', 'id_reserva')
        except Exception as exc:
            flash(f'No se pudieron cargar datos de MySQL: {exc}', 'error')

    return render_template(
        'mysql_panel.html',
        mysql_status=mensaje,
        usuarios=usuarios,
        productos_mysql=productos_mysql,
        reservas_mysql=reservas_mysql,
        negocio_name=BUSINESS_NAME,
    )


@app.route('/mysql/init', methods=['POST'])
@login_required
@owner_required
def mysql_init():
    try:
        mysql_manager.crear_tablas()
        flash('Tablas MySQL creadas/verificadas correctamente.', 'success')
    except Exception as exc:
        flash(f'No se pudo inicializar MySQL: {exc}', 'error')
    return redirect(url_for('mysql_panel'))


@app.route('/mysql/usuarios', methods=['POST'])
@login_required
@owner_required
def mysql_usuarios():
    accion = request.form.get('accion', '').strip().lower()
    try:
        if accion == 'crear':
            nombre = request.form.get('nombre', '').strip()
            email = request.form.get('email', request.form.get('mail', '')).strip().lower()
            password = request.form.get('password', '').strip()
            if not all([nombre, email, password]):
                flash('Completa nombre, email y password.', 'error')
            else:
                mysql_manager.insert_usuario(nombre, email, generate_password_hash(password))
                flash('Usuario MySQL creado correctamente.', 'success')
        elif accion == 'eliminar':
            mysql_manager.delete_usuario(int(request.form.get('id_usuario', 0)))
            flash('Usuario eliminado de MySQL.', 'success')
    except Exception as exc:
        flash(f'Error en usuarios MySQL: {exc}', 'error')
    return redirect(url_for('mysql_panel'))


@app.route('/mysql/productos', methods=['POST'])
@login_required
@owner_required
def mysql_productos():
    accion = request.form.get('accion', '').strip().lower()
    try:
        if accion == 'crear':
            nombre = request.form.get('nombre', '').strip()
            categoria = request.form.get('categoria', '').strip()
            cantidad = int(request.form.get('cantidad', 0))
            precio = float(request.form.get('precio', 0))
            mysql_manager.insert_producto(nombre, categoria, cantidad, precio)
            flash('Producto creado en MySQL.', 'success')
        elif accion == 'eliminar':
            mysql_manager.delete_producto(int(request.form.get('id_producto', 0)))
            flash('Producto eliminado de MySQL.', 'success')
    except Exception as exc:
        flash(f'Error en productos MySQL: {exc}', 'error')
    return redirect(url_for('mysql_panel'))


@app.route('/mysql/reservas', methods=['POST'])
@login_required
@owner_required
def mysql_reservas():
    accion = request.form.get('accion', '').strip().lower()
    try:
        if accion == 'crear':
            cliente = request.form.get('cliente', '').strip()
            telefono = request.form.get('telefono', '').strip()
            email = request.form.get('email', '').strip().lower()
            personas = int(request.form.get('personas', 1))
            fecha_reserva_raw = request.form.get('fecha_reserva', '').strip()
            fecha_reserva = normalize_reserva_datetime(fecha_reserva_raw) if fecha_reserva_raw else None
            cliente = normalize_cliente_nombre(cliente, email, telefono)
            mysql_manager.insert_reserva(cliente, telefono, email, personas, fecha_reserva)
            flash('Reserva creada en MySQL.', 'success')
        elif accion == 'eliminar':
            mysql_manager.delete_reserva(int(request.form.get('id_reserva', 0)))
            flash('Reserva eliminada de MySQL.', 'success')
    except Exception as exc:
        flash(f'Error en reservas MySQL: {exc}', 'error')
    return redirect(url_for('mysql_panel'))


@app.route('/favicon.ico')
def favicon():
    return '', 204


@app.errorhandler(404)
def pagina_no_encontrada(error):
    try:
        return render_template('error_404.html'), 404
    except TemplateNotFound:
        return '404 - Pagina no encontrada', 404


if __name__ == '__main__':
    app.run(debug=True)
