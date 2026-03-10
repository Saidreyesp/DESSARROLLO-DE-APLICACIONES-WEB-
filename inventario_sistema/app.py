from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash
from inventario.bd import db
from inventario.productos import Producto as ProductoORM
from inventario.persistencia import save_txt, save_json, save_csv, read_txt, read_json, read_csv
from models.conexion import ConexionSQLite
from Conexion.conexion import MySQLManager

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

# Configuración
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_inventario_2026'


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
    }

# Inicialización de Bases de Datos
db.init_app(app)
db_conexion = ConexionSQLite()
mysql_manager = MySQLManager()

with app.app_context():
    db.create_all()
    # Tabla local para postulaciones/usuarios de Trabaja con Nosotros
    with sqlite3.connect('inventario.db') as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS usuarios_trabajo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_completo TEXT NOT NULL,
                nombre_usuario TEXT NOT NULL UNIQUE,
                correo TEXT NOT NULL UNIQUE,
                telefono TEXT,
                password TEXT NOT NULL,
                cargo_interes TEXT,
                fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )

    # Si no hay platos en la base, añadimos ejemplos para comenzar
    if not db_conexion.obtener_todos_productos():
        ejemplos = [
            (
                "Pollo Asado",
                20,
                4.00,
                "Asados",
                "Pollo asado al carbon.",
                "https://img.freepik.com/fotos-premium/pollo-asado-arroz-plato-primer-plano_848191-330.jpg?w=2000",
            ),
            (
                "Chuleta Asada",
                20,
                4.00,
                "Asados",
                "Chuleta asada a la parrilla.",
                "https://3.bp.blogspot.com/-49k8Bsu8D_4/WE8QNm0EzEI/AAAAAAAAAD0/h0pnOg3sTuwmLUeTpDDFWfHq5PjkVuyjACLcB/s1600/imagen-arroz-con-menestra.jpg",
            ),
            (
                "Carne Asada",
                20,
                4.00,
                "Asados",
                "Carne asada al punto.",
                "https://th.bing.com/th/id/R.83010750cc93ebe9e790c4dc185ec3d0?rik=z3AlchOZHRb0XQ&pid=ImgRaw&r=0",
            ),
            (
                "Caldo de Gallina",
                20,
                3.50,
                "Caldos",
                "Caldo de gallina tradicional.",
                "https://tse3.mm.bing.net/th/id/OIP.scKWVE-svuaRalRWQE0U_wHaEN?rs=1&pid=ImgDetMain&o=7&rm=3",
            ),
            (
                "Caldo de Pata",
                20,
                3.50,
                "Caldos",
                "Caldo de pata casero.",
                "https://tse3.mm.bing.net/th/id/OIP.IA3dO64bf82YMEnOageqhQHaEK?rs=1&pid=ImgDetMain&o=7&rm=3",
            ),
            (
                "Aguado",
                20,
                3.50,
                "Caldos",
                "Aguado de pollo.",
                "https://www.laylita.com/recipes/wp-content/uploads/2008/05/Aguado-chicken-rice-soup.jpg",
            ),
            (
                "Seco de Gallina",
                20,
                4.00,
                "Tradicional",
                "Seco de gallina con arroz.",
                "https://img-global.cpcdn.com/recipes/c3a1554dbcbd54df/1200x630cq70/photo.jpg",
            ),
            (
                "Seco de Carne",
                20,
                4.00,
                "Tradicional",
                "Seco de carne con arroz.",
                "https://i.ytimg.com/vi/8wIReJqlHvc/maxresdefault.jpg",
            ),
            (
                "Guatita",
                20,
                4.00,
                "Tradicional",
                "Guatita tradicional.",
                "https://www.artecuador.com/images/guatita.jpg",
            ),
            (
                "Lengua Guisada",
                20,
                4.00,
                "Tradicional",
                "Lengua guisada en salsa.",
                "https://i.pinimg.com/originals/85/4c/41/854c412133e56636e2b509a9f842f84b.jpg",
            ),
            (
                "Pollo al Jugo",
                20,
                4.00,
                "Tradicional",
                "Pollo al jugo con salsa casera.",
                "https://tse4.mm.bing.net/th/id/OIP.-tVTzuuu4dNhspRmnyVpswAAAA?rs=1&pid=ImgDetMain&o=7&rm=3",
            ),
            (
                "Gaseosa",
                30,
                0.50,
                "Bebidas",
                "Gaseosa personal fria.",
                "https://source.unsplash.com/1200x900/?cola,soft-drink",
            ),
            (
                "Jugo Quaker",
                25,
                0.50,
                "Bebidas",
                "Jugo de avena estilo Quaker.",
                "https://source.unsplash.com/1200x900/?oat-drink,juice",
            ),
            (
                "Jugo de Tamarindo",
                25,
                0.50,
                "Bebidas",
                "Jugo de tamarindo natural.",
                "https://source.unsplash.com/1200x900/?tamarind,juice",
            ),
            (
                "Gaseosa 1L",
                20,
                1.00,
                "Bebidas",
                "Gaseosa de un litro.",
                "https://source.unsplash.com/1200x900/?cola,bottle",
            ),
        ]
        for nombre, cantidad, precio, categoria, descripcion, imagen in ejemplos:
            db_conexion.añadir_producto(nombre, cantidad, precio, categoria, descripcion, imagen)

# -------------------------------------------------------------------------
# RUTAS PRINCIPALES
# -------------------------------------------------------------------------

@app.route('/')
def index():
    productos = db_conexion.obtener_todos_productos()
    total_productos = len(productos)
    valor_total = db_conexion.obtener_valor_total_inventario()
    bajo_stock = db_conexion.obtener_bajo_stock(5)
    return render_template('index.html', total=total_productos, valor=valor_total, bajo_stock=bajo_stock)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/trabaja-con-nosotros', methods=['GET', 'POST'])
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

        password_hash = generate_password_hash(password)

        try:
            with sqlite3.connect('inventario.db') as conn:
                conn.execute(
                    '''
                    INSERT INTO usuarios_trabajo
                    (nombre_completo, nombre_usuario, correo, telefono, password, cargo_interes)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (nombre_completo, nombre_usuario, correo, telefono, password_hash, cargo_interes),
                )
            flash('Usuario creado correctamente. Ahora envia tu hoja de vida al correo indicado.', 'success')
            return redirect(url_for('trabaja_con_nosotros', creado='1'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario o correo ya existe. Intenta con otro.', 'error')

    with sqlite3.connect('inventario.db') as conn:
        conn.row_factory = sqlite3.Row
        usuarios = conn.execute(
            'SELECT nombre_completo, nombre_usuario, correo, telefono, cargo_interes, fecha_registro FROM usuarios_trabajo ORDER BY id DESC LIMIT 12'
        ).fetchall()

    creado = request.args.get('creado', '0') == '1'
    return render_template('trabaja.html', usuarios=usuarios, creado=creado)

@app.route('/menu')
@app.route('/productos')
def productos():
    productos = db_conexion.obtener_todos_productos()
    bebida_nombres = {'gaseosa', 'gaseosa 1l', 'jugo quaker', 'jugo de tamarindo', 'botella de agua'}
    bebidas = [
        p for p in productos
        if (p.get('categoria', '').lower() == 'bebidas')
        or (p.get('nombre', '').lower() in bebida_nombres)
    ]
    platos = [p for p in productos if p not in bebidas]
    return render_template('productos.html', productos=productos, platos=platos, bebidas=bebidas)


@app.route('/plato/<string:nombre>')
def detalle_plato(nombre):
    producto = next((p for p in db_conexion.obtener_todos_productos() if p.get('nombre') == nombre), None)
    return render_template('plato.html', plato=producto, nombre=nombre)


@app.route('/producto/<int:id>')
def producto_detalle(id):
    producto = db_conexion.obtener_producto(id)
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos'))
    return render_template('producto_detalle.html', producto=producto)


@app.route('/buscar', methods=['GET'])
def buscar():
    termino = request.args.get('termino', '').strip()
    resultados = db_conexion.buscar_producto(termino) if termino else []
    return render_template('buscar.html', termino=termino, resultados=resultados)

# -------------------------------------------------------------------------
# RUTAS DE RESERVAS (CORREGIDAS)
# -------------------------------------------------------------------------

@app.route('/reserva', defaults={'cliente': ''})
@app.route('/reserva/<cliente>')
def reserva(cliente):
    # Esta ruta muestra el formulario (vacío o con nombre del link)
    return render_template('reserva.html', cliente=cliente)

@app.route('/reserva/confirmar', methods=['POST'])
def confirmar_reserva():
    # Recibimos los datos del formulario de reserva
    nombre = request.form.get('cliente')
    personas = request.form.get('personas')
    fecha = request.form.get('fecha_reserva')
    telefono = request.form.get('telefono')
    email = request.form.get('email')

    mensaje_exito = f"¡Gracias {nombre}! Tu reserva para {personas} personas el día {fecha} ha sido confirmada correctamente."
    
    # Persistencia de la reserva en JSON (Semana 12)
    registro_reserva = {
        "tipo": "RESERVA",
        "cliente": nombre,
        "personas": personas,
        "fecha": fecha,
        "contacto": telefono
    }
    save_json(registro_reserva)

    return render_template('reserva.html', cliente=nombre, mensaje=mensaje_exito)

# -------------------------------------------------------------------------
# RUTAS CRUD PRODUCTOS
# -------------------------------------------------------------------------

@app.route('/producto/nuevo', methods=['GET', 'POST'])
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
            save_txt(record); save_json(record); save_csv(record)
            flash(f'Plato "{nombre}" añadido exitosamente.', 'success')
            return redirect(url_for('productos'))
    
    return render_template('producto_form.html')

@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
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
            flash(f'Plato actualizado exitosamente.', 'success')
            return redirect(url_for('productos'))
            
    return render_template('producto_editar.html', producto=producto)

@app.route('/producto/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if db_conexion.eliminar_producto(id):
        flash('Plato eliminado.', 'success')
    return redirect(url_for('productos'))

# -------------------------------------------------------------------------
# REPORTES Y DATOS
# -------------------------------------------------------------------------

@app.route('/reportes')
def reportes():
    productos = db_conexion.obtener_todos_productos()
    valor_total = db_conexion.obtener_valor_total_inventario()
    cantidad_total = sum(p.get('cantidad', 0) for p in productos)
    bajo_stock = db_conexion.obtener_bajo_stock(5)
    return render_template(
        'reportes.html',
        total_productos=len(productos),
        valor_total=valor_total,
        cantidad_total=cantidad_total,
        bajo_stock=bajo_stock,
        productos=productos,
    )

@app.route('/datos')
def listar_datos():
    return render_template('datos.html', txt=read_txt(), json_data=read_json(), csv=read_csv(), db_items=ProductoORM.query.all())


@app.route('/mysql', methods=['GET'])
def mysql_panel():
    ok, status_msg = mysql_manager.ping()

    usuarios = []
    productos_mysql = []
    reservas_mysql = []

    if ok:
        try:
            usuarios = mysql_manager.fetch_all('usuarios', 'id_usuario')
            productos_mysql = mysql_manager.fetch_all('productos_mysql', 'id_producto')
            reservas_mysql = mysql_manager.fetch_all('reservas_mysql', 'id_reserva')
        except Exception as exc:
            status_msg = f'Conectado, pero no se pudo consultar tablas: {exc}'

    return render_template(
        'mysql_panel.html',
        mysql_ok=ok,
        mysql_status=status_msg,
        usuarios=usuarios,
        productos_mysql=productos_mysql,
        reservas_mysql=reservas_mysql,
    )


@app.route('/mysql/init', methods=['POST'])
def mysql_init_tables():
    try:
        mysql_manager.crear_tablas()
        flash('Tablas MySQL creadas correctamente.', 'success')
    except Exception as exc:
        flash(f'No se pudo crear tablas MySQL: {exc}', 'error')
    return redirect(url_for('mysql_panel'))


@app.route('/mysql/usuarios', methods=['POST'])
def mysql_usuarios_crud():
    accion = request.form.get('accion', 'crear')
    try:
        if accion == 'crear':
            mysql_manager.insert_usuario(
                request.form.get('nombre', '').strip(),
                request.form.get('mail', '').strip(),
                request.form.get('password', '').strip(),
            )
            flash('Usuario creado en MySQL.', 'success')
        elif accion == 'editar':
            mysql_manager.update_usuario(
                int(request.form.get('id_usuario', 0)),
                request.form.get('nombre', '').strip(),
                request.form.get('mail', '').strip(),
                request.form.get('password', '').strip(),
            )
            flash('Usuario actualizado en MySQL.', 'success')
        elif accion == 'eliminar':
            mysql_manager.delete_usuario(int(request.form.get('id_usuario', 0)))
            flash('Usuario eliminado en MySQL.', 'success')
    except Exception as exc:
        flash(f'Operacion usuarios MySQL fallo: {exc}', 'error')

    return redirect(url_for('mysql_panel'))


@app.route('/mysql/productos', methods=['POST'])
def mysql_productos_crud():
    accion = request.form.get('accion', 'crear')
    try:
        if accion == 'crear':
            mysql_manager.insert_producto(
                request.form.get('nombre', '').strip(),
                request.form.get('categoria', '').strip(),
                int(request.form.get('cantidad', 0)),
                float(request.form.get('precio', 0)),
            )
            flash('Producto MySQL creado.', 'success')
        elif accion == 'editar':
            mysql_manager.update_producto(
                int(request.form.get('id_producto', 0)),
                request.form.get('nombre', '').strip(),
                request.form.get('categoria', '').strip(),
                int(request.form.get('cantidad', 0)),
                float(request.form.get('precio', 0)),
            )
            flash('Producto MySQL actualizado.', 'success')
        elif accion == 'eliminar':
            mysql_manager.delete_producto(int(request.form.get('id_producto', 0)))
            flash('Producto MySQL eliminado.', 'success')
    except Exception as exc:
        flash(f'Operacion productos MySQL fallo: {exc}', 'error')

    return redirect(url_for('mysql_panel'))


@app.route('/mysql/reservas', methods=['POST'])
def mysql_reservas_crud():
    accion = request.form.get('accion', 'crear')
    try:
        if accion == 'crear':
            mysql_manager.insert_reserva(
                request.form.get('cliente', '').strip(),
                request.form.get('telefono', '').strip(),
                int(request.form.get('personas', 1)),
                request.form.get('fecha_reserva', '').strip() or None,
            )
            flash('Reserva MySQL creada.', 'success')
        elif accion == 'editar':
            mysql_manager.update_reserva(
                int(request.form.get('id_reserva', 0)),
                request.form.get('cliente', '').strip(),
                request.form.get('telefono', '').strip(),
                int(request.form.get('personas', 1)),
                request.form.get('fecha_reserva', '').strip() or None,
            )
            flash('Reserva MySQL actualizada.', 'success')
        elif accion == 'eliminar':
            mysql_manager.delete_reserva(int(request.form.get('id_reserva', 0)))
            flash('Reserva MySQL eliminada.', 'success')
    except Exception as exc:
        flash(f'Operacion reservas MySQL fallo: {exc}', 'error')

    return redirect(url_for('mysql_panel'))

# -------------------------------------------------------------------------
# MANEJO DE ERRORES E INICIO
# -------------------------------------------------------------------------

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error_404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)