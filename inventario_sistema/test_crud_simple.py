import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from models.producto import Producto
print('Producto importado exitosamente')

from models.inventario import Inventario
print('Inventario importado exitosamente')

from models.conexion import ConexionSQLite
print('ConexionSQLite importado exitosamente')

print('TODOS LOS IMPORTS EXITOSOS')