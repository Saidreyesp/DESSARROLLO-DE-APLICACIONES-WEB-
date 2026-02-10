from flask import Flask, render_template

app = Flask(__name__)

# Ruta principal
@app.route("/")
def inicio():
    return render_template("index.html")

# Ruta dinámica (ejemplo pedido en el deber)
@app.route("/plato/<nombre>")
def plato(nombre):
    return f"Plato seleccionado: {nombre} - Restaurante El Gran Sabor"

if __name__ == "__main__":
    app.run(debug=True)
