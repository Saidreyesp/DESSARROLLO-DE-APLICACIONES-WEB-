from flask import Flask, render_template, request, redirect, url_for
from inventario.bd import db
from inventario.productos import Producto as ProductoORM

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_inventario_2026'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', total=0, valor=0.0, bajo_stock=[])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/productos')
def productos():
    return render_template('productos.html', productos=[])

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        return redirect(url_for('productos'))
    return render_template('producto_form.html')

@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = {'id': id, 'nombre': 'Test', 'cantidad': 0, 'precio': 0}
    if request.method == 'POST':
        return redirect(url_for('productos'))
    return render_template('producto_editar.html', producto=producto)

@app.route('/producto/<int:id>')
def ver_producto(id):
    producto = {'id': id, 'nombre': 'Test', 'cantidad': 0, 'precio': 0}
    return render_template('producto_detalle.html', producto=producto)

@app.route('/producto/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    return redirect(url_for('productos'))

@app.route('/buscar', methods=['GET'])
def buscar():
    termin = request.args.get('termino', '')
    return render_template('buscar.html', termino=termin, resultados=[])

@app.route('/bajo-stock')
def bajo_stock():
    return render_template('bajo_stock.html', productos=[], minimo=5)

@app.route('/reportes')
def reportes():
    return render_template('reportes.html',
                          total_productos=0,
                          valor_total=0.0,
                          cantidad_total=0,
                          bajo_stock=[],
                          productos=[])

@app.route('/datos')
def listar_datos():
    return render_template('datos.html', txt=[], json_data=[], csv=[], db_items=[])

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def error_servidor(error):
    return render_template('error_500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
