import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from models.producto import Producto
from models.inventario import Inventario
from models.conexion import ConexionSQLite

def test_producto():
    print("\n" + "=" * 60)
    print("TEST 1: PRODUCTO")
    print("=" * 60)
    p = Producto(1, 'Pasta Carbonara', 10, 15.99)
    print(p)
    p.set_cantidad(-5)
    print(f"Cantidad ajustada (no negativa): {p.get_cantidad()}")
    return True

def test_inventario():
    print("\n" + "=" * 60)
    print("TEST 2: INVENTARIO")
    print("=" * 60)
    inv = Inventario()
    p1 = Producto(1, 'Pasta', 5, 10.0)
    p2 = Producto(2, 'Ensalada', 3, 8.0)
    inv.aniadir_producto(p1)
    inv.aniadir_producto(p2)
    print(f"Cantidad productos: {inv.cantidad_productos()}")
    print(f"Buscar 'Pasta': {[x.get_nombre() for x in inv.buscar_producto('Pasta')]}")
    return True

def test_sqlite():
    print("\n" + "=" * 60)
    print("TEST 3: SQLITE")
    print("=" * 60)
    db = ConexionSQLite(':memory:')
    id1 = db.añadir_producto('Pasta', 5, 10.0)
    print(f"Insertado ID: {id1}")
    result = db.obtener_producto(id1)
    print(f"Obtenido: {result}")
    db.actualizar_producto(id1, cantidad=2)
    print(f"Actualizado: {db.obtener_producto(id1)}")
    db.eliminar_producto(id1)
    print(f"Despues eliminar, obtener: {db.obtener_producto(id1)}")
    return True

def main():
    for test in (test_producto, test_inventario, test_sqlite):
        if not test():
            print("Test failed")
            return
    print("All tests passed")

if __name__ == '__main__':
    main()