from flask import Flask, render_template, request, redirect, url_for

# mantenemos compatibilidad con los modelos originales
from models.producto import Producto as SimpleProducto
from models.inventario import Inventario
from models.conexion import ConexionSQLite

# SQLAlchemy y persistencia en archivos
from inventario.bd import db
from inventario.productos import Producto
from inventario.persistencia import save_txt, save_json, save_csv, read_txt, read_json, read_csv

app = Flask(__name__)

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/productos')
def productos():
    db_items = Producto.query.all()
    return render_template('productos.html', productos=db_items)

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        precio = request.form.get('precio') or 0
        cantidad = request.form.get('cantidad') or 0
        record = {'nombre': nombre, 'precio': float(precio), 'cantidad': int(cantidad)}

        # Guardar en archivos
        save_txt(record)
        save_json(record)
        save_csv(record)

        # Guardar en DB (SQLAlchemy)
        p = Producto(nombre=record['nombre'], precio=record['precio'], cantidad=record['cantidad'])
        db.session.add(p)
        db.session.commit()

        return redirect(url_for('listar_datos'))
    return render_template('producto_form.html')

@app.route('/datos')
def listar_datos():
    txt = read_txt()
    js = read_json()
    csv = read_csv()
    db_items = Producto.query.all()
    return render_template('datos.html', txt=txt, json_data=js, csv=csv, db_items=db_items)

if __name__ == '__main__':
    app.run(debug=True)
