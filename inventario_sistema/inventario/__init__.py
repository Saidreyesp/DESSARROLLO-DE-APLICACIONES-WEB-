# Paquete Inventario
"""
Módulo de Inventario - Sistema de gestión de productos con múltiples fuentes de persistencia.

Proporciona:
- Modelos de datos (Producto)
- Gestión de inventario (GestorInventario)
- Persistencia en múltiples formatos (TXT, JSON, CSV, SQLite)
"""

from inventario.bd import db
from inventario.productos import Producto
from inventario.inventario import GestorInventario
from inventario.persistencia import save_txt, save_json, save_csv, read_txt, read_json, read_csv

__all__ = [
    'db',
    'Producto',
    'GestorInventario',
    'save_txt', 'read_txt',
    'save_json', 'read_json',
    'save_csv', 'read_csv'
]
