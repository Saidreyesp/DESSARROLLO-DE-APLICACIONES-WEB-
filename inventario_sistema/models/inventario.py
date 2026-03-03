"""Modulo de Inventario"""

class Inventario:
    def __init__(self):
        self.productos = {}
        self.ids_activos = set()
        self.categorias = ('Electr\u00f3nica', 'Ferreter\u00eda', 'Alimentos', 'Ropa', 'Otros')

    def aniadir_producto(self, producto):
        if producto.get_id() not in self.productos:
            self.productos[producto.get_id()] = producto
            self.ids_activos.add(producto.get_id())
            return True
        return False

    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]
            self.ids_activos.discard(id)
            return True
        return False

    def obtener_producto(self, id):
        return self.productos.get(id)

    def buscar_producto(self, nombre):
        return [p for p in self.productos.values() if nombre.lower() in p.get_nombre().lower()]

    def cantidad_productos(self):
        return len(self.productos)