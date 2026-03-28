from datetime import datetime
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
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
    productos = ProductoORM.query.order_by(ProductoORM.id.asc()).all()
    total_productos = len(productos)
    cantidad_total = sum(int(p.cantidad or 0) for p in productos)
    valor_total = sum(float(p.precio or 0) * int(p.cantidad or 0) for p in productos)
    bajo_stock = [p for p in productos if int(p.cantidad or 0) < 5]

    return render_template('reportes.html',
                          total_productos=total_productos,
                          valor_total=valor_total,
                          cantidad_total=cantidad_total,
                          bajo_stock=bajo_stock,
                          productos=productos,
                          negocio_name='Comedor Alexandra')


@app.route('/reportes/pdf')
def reporte_pdf():
    productos = ProductoORM.query.order_by(ProductoORM.id.asc()).all()
    total_items = len(productos)
    total_stock = sum(int(p.cantidad or 0) for p in productos)
    total_valor = sum(float(p.precio or 0) * int(p.cantidad or 0) for p in productos)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    _, height = A4

    y = height - 50
    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawString(40, y, 'Reporte de Inventario (SQLite)')
    y -= 18
    pdf.setFont('Helvetica', 10)
    pdf.drawString(40, y, f'Fecha de emision: {datetime.now().strftime("%Y-%m-%d %H:%M")}')
    y -= 16
    pdf.drawString(40, y, f'Total items: {total_items} | Stock total: {total_stock} | Valor total: ${total_valor:.2f}')
    y -= 24

    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(40, y, 'ID')
    pdf.drawString(70, y, 'Nombre')
    pdf.drawString(280, y, 'Categoria')
    pdf.drawRightString(420, y, 'Cantidad')
    pdf.drawRightString(520, y, 'Precio')
    y -= 12
    pdf.setFont('Helvetica', 9)

    for producto in productos:
        if y < 60:
            pdf.showPage()
            y = height - 50
            pdf.setFont('Helvetica-Bold', 9)
            pdf.drawString(40, y, 'ID')
            pdf.drawString(70, y, 'Nombre')
            pdf.drawString(280, y, 'Categoria')
            pdf.drawRightString(420, y, 'Cantidad')
            pdf.drawRightString(520, y, 'Precio')
            y -= 12
            pdf.setFont('Helvetica', 9)

        pdf.drawString(40, y, str(producto.id))
        pdf.drawString(70, y, (producto.nombre or '')[:38])
        pdf.drawString(280, y, (producto.categoria or '-')[:22])
        pdf.drawRightString(420, y, str(int(producto.cantidad or 0)))
        pdf.drawRightString(520, y, f'${float(producto.precio or 0):.2f}')
        y -= 14

    pdf.save()
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='reporte_inventario.pdf',
    )

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
