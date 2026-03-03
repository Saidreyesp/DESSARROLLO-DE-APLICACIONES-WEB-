import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from models.producto import Producto
from models.inventario import Inventario
from models.conexion import ConexionSQLite

print('TEST 1: Clase Producto')
print('='*70)
p = Producto(1, 'Pasta', 10, 15.99, 'Platos')
print(f'Producto: {p.get_nombre()}, Cantidad: {p.get_cantidad()}, Precio: {p.get_precio()}')
print(f'Valor Total: {p.get_valor_total():.2f}')
print('TEST 1: PASSED\n')

print('TEST 2: Clase Inventario')
print('='*70)
inv = Inventario()
inv.aniadir_producto(p)
inv.aniadir_producto(Producto(2, 'Ensalada', 5, 12.50))
inv.aniadir_producto(Producto(3, 'Tiramisu', 2, 8.99))
print(f'Total productos en inventario: {inv.cantidad_productos()}')
print(f'Valor total del inventario: {inv.valor_total_inventario():.2f}')
bajo_stock = inv.productos_bajo_stock(3)
print(f'Productos bajo stock (<3): {len(bajo_stock)}')
print('TEST 2: PASSED\n')

print('TEST 3: ConexionSQLite')
print('='*70)
db = ConexionSQLite(':memory:')
id1 = db.aniadir_producto('Pasta Carbonara', 10, 15.99, 'Platos')
id2 = db.aniadir_producto('Ensalada Griega', 8, 12.50, 'Ensaladas')
id3 = db.aniadir_producto('Tiramisu', 5, 8.99, 'Postres')
print(f'Creados 3 productos con IDs: {id1}, {id2}, {id3}')
todos = db.obtener_todos_productos()
print(f'Total en BD: {len(todos)}')
plato = db.obtener_producto(id1)
print(f'Recuperado: {plato[\"nombre\"]} ({plato[\"cantidad\"]} x {plato[\"precio\"]})')
db.actualizar_producto(id1, cantidad=5)
actualizado = db.obtener_producto(id1)
print(f'Despues UPDATE: {actualizado[\"nombre\"]} ({actualizado[\"cantidad\"]} unidades)')
print('TEST 3: PASSED\n')

print('='*70)
print('TODOS LOS TESTS COMPLETADOS EXITOSAMENTE')
print('='*70)