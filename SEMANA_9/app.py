from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Ruta para la página de productos
@app.route('/productos')
def productos():
    return render_template('productos.html')

if __name__ == "__main__":
    app.run(debug=True)
