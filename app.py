from flask import Flask, render_template, request, redirect, url_for, flash
from inventario.bd import db
from inventario.productos import Producto as ProductoORM
from inventario.persistencia import save_txt, save_json, save_csv, read_txt, read_json, read_csv
from models.conexion import ConexionSQLite

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_inventario_2026'

db.init_app(app)
db_conexion = ConexionSQLite()

with app.app_context():
    db.create_all()
    # si no hay platos en la base, añadimos algunos ejemplos para comenzar
    if not db_conexion.obtener_todos_productos():
        ejemplos = [
            ("Seco de Pollo", 10, 8.50, "Sopas", "Delicioso pollo guisado con arroz"),
            ("Encebollado", 15, 6.75, "Pescados", "Sopa de pescado con yuca y cebolla"),
            ("Ceviche de Camarón", 20, 9.00, "Mariscos", "Camarones frescos en jugo cítrico"),
            ("Asado de Ternasco", 12, 11.00, "Carnes", "Lomitos de ternasco acompañados de papas"),
            ("Hornado", 8, 10.00, "Carnes", "Cerdo asado con mote y llapingachos"),
            ("Asados Mixtos", 7, 12.50, "Carnes", "Variedad de carnes asadas al estilo Quevedo"),
        ]
        for nombre,cantidad,precio,categoria,descripcion in ejemplos:
            db_conexion.añadir_producto(nombre,cantidad,precio,categoria,descripcion)

@app.route('/')
def index():
    productos = db_conexion.obtener_todos_productos()
    total_productos = len(productos)
    valor_total = db_conexion.obtener_valor_total_inventario()
    bajo_stock = db_conexion.obtener_bajo_stock(5)
    # Cambiado para tema Restaurante
    return render_template('index.html', total=total_productos, valor=valor_total, bajo_stock=bajo_stock, negocio_name='Restaurante La Buena Mesa')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/productos')
def productos():
    # mantener compatibilidad; mostrar Menú de platos
    productos = db_conexion.obtener_todos_productos()
    return render_template('productos.html', productos=productos, negocio_name='Restaurante La Buena Mesa')


@app.route('/menu')
def menu():
    productos = db_conexion.obtener_todos_productos()
    return render_template('productos.html', productos=productos, negocio_name='Restaurante La Buena Mesa')


@app.route('/plato/<nombre>')
def ver_plato(nombre):
    # búsqueda simple por nombre (case-insensitive)
    resultados = db_conexion.buscar_producto(nombre)
    plato = resultados[0] if resultados else None
    return render_template('plato.html', plato=plato, nombre=nombre, negocio_name='Restaurante La Buena Mesa')

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cantidad = int(request.form.get('cantidad', 0))
        precio = float(request.form.get('precio', 0))
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')
        
        id_nuevo = db_conexion.añadir_producto(nombre, cantidad, precio, categoria, descripcion)
        
        if id_nuevo > 0:
            record = {'id': id_nuevo, 'nombre': nombre, 'cantidad': cantidad, 'precio': precio}
            save_txt(record)
            save_json(record)
            save_csv(record)
            flash(f'Producto "{nombre}" añadido exitosamente.', 'success')
            return redirect(url_for('productos'))
        else:
            flash(f'Error: No se pudo añadir el producto.', 'error')
    
    return render_template('producto_form.html')

@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = db_conexion.obtener_producto(id)
    
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cantidad = int(request.form.get('cantidad', 0))
        precio = float(request.form.get('precio', 0))
        categoria = request.form.get('categoria')
        descripcion = request.form.get('descripcion')
        
        if db_conexion.actualizar_producto(id, nombre, cantidad, precio, categoria, descripcion):
            flash(f'Producto actualizado exitosamente.', 'success')
            return redirect(url_for('ver_producto', id=id))
        else:
            flash('Error al actualizar el producto.', 'error')
    
    return render_template('producto_editar.html', producto=producto)

@app.route('/producto/<int:id>')
def ver_producto(id):
    producto = db_conexion.obtener_producto(id)
    
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos'))
    
    return render_template('producto_detalle.html', producto=producto)

@app.route('/producto/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = db_conexion.obtener_producto(id)
    
    if not producto:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('productos'))
    
    if db_conexion.eliminar_producto(id):
        flash(f'Producto "{producto["nombre"]}" eliminado exitosamente.', 'success')
    else:
        flash('Error al eliminar el producto.', 'error')
    
    return redirect(url_for('productos'))

@app.route('/buscar', methods=['GET'])
def buscar():
    termino = request.args.get('termino', '').strip()
    resultados = []
    
    if termino:
        resultados = db_conexion.buscar_producto(termino)
    
    return render_template('buscar.html', termino=termino, resultados=resultados, negocio_name='Restaurante La Buena Mesa')


@app.route('/reserva/<cliente>')
def reserva_cliente(cliente):
    mensaje = f'Bienvenido, {cliente}. Tu reserva en Restaurante La Buena Mesa está en proceso.'
    return render_template('reserva.html', cliente=cliente, mensaje=mensaje, negocio_name='Restaurante La Buena Mesa')

@app.route('/bajo-stock')
def bajo_stock():
    minimo = request.args.get('minimo', 5, type=int)
    productos = db_conexion.obtener_bajo_stock(minimo)
    return render_template('bajo_stock.html', productos=productos, minimo=minimo)

@app.route('/reportes')
def reportes():
    productos = db_conexion.obtener_todos_productos()
    total_productos = len(productos)
    valor_total = db_conexion.obtener_valor_total_inventario()
    bajo_stock = db_conexion.obtener_bajo_stock(5)
    cantidad_total = sum(p['cantidad'] for p in productos) if productos else 0
    
    return render_template('reportes.html',
                          total_productos=total_productos,
                          valor_total=valor_total,
                          cantidad_total=cantidad_total,
                          bajo_stock=bajo_stock,
                          productos=productos)

@app.route('/datos')
def listar_datos():
    txt = read_txt()
    js = read_json()
    csv = read_csv()
    db_items = ProductoORM.query.all()
    return render_template('datos.html', txt=txt, json_data=js, csv=csv, db_items=db_items, negocio_name='Restaurante La Buena Mesa')

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def error_servidor(error):
    return render_template('error_500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
