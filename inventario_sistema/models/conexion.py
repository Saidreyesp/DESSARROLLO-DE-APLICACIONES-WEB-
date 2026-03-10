"""Módulo de Conexión SQLite - Gestiona todas las operaciones con la base de datos."""

import sqlite3
import os


class ConexionSQLite:
    """Clase que gestiona la conexión y operaciones CRUD en SQLite.

    Proporciona métodos para interactuar con la base de datos de inventario
    incluyendo creación de tablas, CRUD de productos, búsqueda y reportes.
    """

    def __init__(self, db_path='inventario.db'):
        """Inicializa la conexión a SQLite."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        """Crea las tablas necesarias si no existen."""
        try:
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                cantidad INTEGER NOT NULL DEFAULT 0,
                precio REAL NOT NULL DEFAULT 0.0,
                categoria TEXT,
                descripcion TEXT,
                imagen TEXT,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')

            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT
            )''')

            # Migracion ligera para bases antiguas que no tienen el campo imagen.
            self.cursor.execute("PRAGMA table_info(productos)")
            columnas = {row[1] for row in self.cursor.fetchall()}
            if 'imagen' not in columnas:
                self.cursor.execute('ALTER TABLE productos ADD COLUMN imagen TEXT')

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear tablas: {e}")

    def añadir_producto(self, nombre, cantidad, precio, categoria=None, descripcion=None, imagen=None):
        """Añade un nuevo producto a la base de datos."""
        try:
            self.cursor.execute('''
            INSERT INTO productos (nombre, cantidad, precio, categoria, descripcion, imagen)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (nombre, cantidad, precio, categoria, descripcion, imagen))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            print(f"Error: El producto '{nombre}' ya existe.")
            return -1
        except sqlite3.Error as e:
            print(f"Error al añadir producto: {e}")
            return -1

    def obtener_producto(self, id):
        """Obtiene un producto por su ID."""
        self.cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def obtener_todos_productos(self):
        """Obtiene todos los productos de la base de datos."""
        self.cursor.execute('SELECT * FROM productos ORDER BY nombre')
        return [dict(row) for row in self.cursor.fetchall()]

    def eliminar_producto(self, id):
        """Elimina un producto por su ID."""
        try:
            self.cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar producto: {e}")
            return False

    def actualizar_producto(self, id, nombre=None, cantidad=None, precio=None, categoria=None, descripcion=None, imagen=None):
        """Actualiza los datos de un producto existente."""
        try:
            updates = []
            params = []

            if nombre is not None:
                updates.append('nombre = ?')
                params.append(nombre)
            if cantidad is not None:
                updates.append('cantidad = ?')
                params.append(max(0, cantidad))
            if precio is not None:
                updates.append('precio = ?')
                params.append(max(0, precio))
            if categoria is not None:
                updates.append('categoria = ?')
                params.append(categoria)
            if descripcion is not None:
                updates.append('descripcion = ?')
                params.append(descripcion)
            if imagen is not None:
                updates.append('imagen = ?')
                params.append(imagen)

            if updates:
                updates.append('fecha_actualizacion = CURRENT_TIMESTAMP')
                params.append(id)
                query = f"UPDATE productos SET {', '.join(updates)} WHERE id = ?"
                self.cursor.execute(query, params)
                self.conn.commit()
                return self.cursor.rowcount > 0
            return False
        except sqlite3.Error as e:
            print(f"Error al actualizar producto: {e}")
            return False

    def buscar_producto(self, termino):
        """Busca productos por nombre o descripción."""
        query = "SELECT * FROM productos WHERE nombre LIKE ? OR descripcion LIKE ? ORDER BY nombre"
        termino_busqueda = f"%{termino}%"
        try:
            self.cursor.execute(query, (termino_busqueda, termino_busqueda))
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error en búsqueda: {e}")
            return []

    def obtener_bajo_stock(self, minimo=5):
        """Obtiene productos con cantidad menor al mínimo especificado."""
        self.cursor.execute('SELECT * FROM productos WHERE cantidad < ? ORDER BY cantidad', (minimo,))
        return [dict(row) for row in self.cursor.fetchall()]

    def obtener_valor_total_inventario(self):
        """Calcula el valor total del inventario."""
        self.cursor.execute('SELECT SUM(cantidad * precio) as total FROM productos')
        row = self.cursor.fetchone()
        return row[0] if row[0] else 0.0

    def mostrar_inventario(self):
        """Imprime el inventario completo de forma formateada."""
        try:
            productos = self.obtener_todos_productos()
            print("\n" + "="*100)
            print("INVENTARIO DESDE SQLite")
            print("="*100)
            if not productos:
                print("El inventario está vacío.")
            else:
                for p in productos:
                    valor_total = p['cantidad'] * p['precio']
                    print(f"ID: {p['id']:3d} | {p['nombre']:20s} | Qty: {p['cantidad']:5d} | "
                          f"${p['precio']:8.2f} | Total: ${valor_total:10.2f}")
            print(f"\nValor total del inventario: ${self.obtener_valor_total_inventario():.2f}")
            print("="*100 + "\n")
        except Exception as e:
            print(f"Error al mostrar inventario: {e}")

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
