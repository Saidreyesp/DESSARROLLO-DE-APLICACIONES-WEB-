import json
import os
from contextlib import contextmanager
from urllib.parse import unquote, urlparse


class MySQLManager:
    """Gestiona conexion, creacion de tablas y operaciones CRUD en MySQL."""

    DEFAULT_HOST = "trolley.proxy.rlwy.net"
    DEFAULT_USER = "root"
    DEFAULT_PASSWORD = "NmDTiUHKZaBALGwDUvSiSqvXGIBOODJs"
    DEFAULT_DATABASE = "railway"
    DEFAULT_PORT = 14574

    def __init__(self):
        self.host = self.DEFAULT_HOST
        self.user = self.DEFAULT_USER
        self.password = self.DEFAULT_PASSWORD
        self.database = self.DEFAULT_DATABASE
        self.port = self.DEFAULT_PORT

        # Railway puede entregar credenciales como URL completa.
        mysql_url = os.getenv("MYSQL_URL", "").strip()
        if mysql_url:
            parsed = urlparse(mysql_url)
            if parsed.scheme.startswith("mysql"):
                self.host = parsed.hostname or self.host
                self.user = unquote(parsed.username or self.user)
                self.password = unquote(parsed.password or self.password)
                self.database = (parsed.path or "/").lstrip("/") or self.database
                if parsed.port:
                    self.port = int(parsed.port)

        # Variables individuales siempre tienen prioridad si existen.
        self.host = os.getenv("MYSQL_HOST", self.host)
        self.user = os.getenv("MYSQL_USER", self.user)
        self.password = os.getenv("MYSQL_PASSWORD", self.password)
        self.database = os.getenv("MYSQL_DATABASE", self.database)
        self.port = int(os.getenv("MYSQL_PORT", str(self.port)))

        # Evita errores comunes cuando el sistema tiene MYSQL_HOST=127.0.0.1 global.
        if self.host.strip().lower() in {"127.0.0.1", "localhost"} and self.port == 3306:
            self.host = self.DEFAULT_HOST
            self.user = self.DEFAULT_USER
            self.password = self.DEFAULT_PASSWORD
            self.database = self.DEFAULT_DATABASE
            self.port = self.DEFAULT_PORT

    def _import_connector(self):
        try:
            import mysql.connector  # type: ignore
            return mysql.connector
        except Exception:
            return None

    @contextmanager
    def connection(self):
        connector = self._import_connector()
        if connector is None:
            raise RuntimeError("mysql-connector-python no esta instalado. Ejecuta: pip install mysql-connector-python")

        conn = connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            connection_timeout=10,
        )
        try:
            yield conn
        finally:
            conn.close()

    def ping(self):
        try:
            with self.connection() as conn:
                return conn.is_connected(), "Conexion MySQL activa"
        except Exception as exc:
            return False, str(exc)

    def crear_tablas(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(120) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS productos_mysql (
                id_producto INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(120) NOT NULL,
                categoria VARCHAR(80),
                cantidad INT NOT NULL DEFAULT 0,
                precio DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS reservas_mysql (
                id_reserva INT AUTO_INCREMENT PRIMARY KEY,
                cliente VARCHAR(120) NOT NULL,
                telefono VARCHAR(30),
                email VARCHAR(150),
                personas INT NOT NULL DEFAULT 1,
                fecha_reserva DATETIME,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                cedula VARCHAR(20) NOT NULL UNIQUE,
                nombres VARCHAR(120) NOT NULL,
                telefono VARCHAR(20),
                email VARCHAR(150),
                direccion VARCHAR(180)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS facturas (
                id_factura INT AUTO_INCREMENT PRIMARY KEY,
                id_cliente INT NOT NULL,
                fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                subtotal DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                iva DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                total DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                metodo_pago VARCHAR(40) NOT NULL DEFAULT 'Efectivo',
                detalle_pago TEXT NULL,
                CONSTRAINT fk_facturas_cliente
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
                    ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS detalle_factura (
                id_detalle INT AUTO_INCREMENT PRIMARY KEY,
                id_factura INT NOT NULL,
                id_producto INT NOT NULL,
                cantidad INT NOT NULL DEFAULT 1,
                precio_unitario DECIMAL(10,2) NOT NULL DEFAULT 0.00,
                CONSTRAINT fk_detalle_factura
                    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT fk_detalle_producto
                    FOREIGN KEY (id_producto) REFERENCES productos_mysql(id_producto)
                    ON UPDATE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
        ]

        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            for q in queries:
                cur.execute(q)

            # Compatibilidad con versiones anteriores que usaban columna "mail".
            cur.execute("SHOW COLUMNS FROM usuarios LIKE 'email'")
            col_email = cur.fetchone()
            cur.execute("SHOW COLUMNS FROM usuarios LIKE 'mail'")
            col_mail = cur.fetchone()
            if not col_email and col_mail:
                cur.execute("ALTER TABLE usuarios ADD COLUMN email VARCHAR(150) NULL")
                cur.execute("UPDATE usuarios SET email = mail WHERE email IS NULL")
                cur.execute("ALTER TABLE usuarios MODIFY email VARCHAR(150) NOT NULL")

            cur.execute("SHOW COLUMNS FROM facturas LIKE 'metodo_pago'")
            col_metodo_pago = cur.fetchone()
            if not col_metodo_pago:
                cur.execute("ALTER TABLE facturas ADD COLUMN metodo_pago VARCHAR(40) NOT NULL DEFAULT 'Efectivo'")

            cur.execute("SHOW COLUMNS FROM facturas LIKE 'detalle_pago'")
            col_detalle_pago = cur.fetchone()
            if not col_detalle_pago:
                cur.execute("ALTER TABLE facturas ADD COLUMN detalle_pago TEXT NULL")

            cur.execute("SHOW COLUMNS FROM reservas_mysql LIKE 'email'")
            col_reserva_email = cur.fetchone()
            if not col_reserva_email:
                cur.execute("ALTER TABLE reservas_mysql ADD COLUMN email VARCHAR(150) NULL AFTER telefono")

            conn.commit()

    def fetch_all(self, table_name, id_column):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(f"SELECT * FROM {table_name} ORDER BY {id_column} DESC")
            return cur.fetchall()

    def fetch_where(self, table_name, where_clause, params=(), order_by=None, limit=None):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {table_name} WHERE {where_clause}"
            if order_by:
                query += f" ORDER BY {order_by}"
            if limit is not None:
                query += " LIMIT %s"
                params = tuple(params) + (int(limit),)
            cur.execute(query, params)
            return cur.fetchall()

    def insert_usuario(self, nombre, email, password):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, password),
            )
            conn.commit()

    def update_usuario(self, id_usuario, nombre, email, password):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE usuarios SET nombre=%s, email=%s, password=%s WHERE id_usuario=%s",
                (nombre, email, password, id_usuario),
            )
            conn.commit()

    def get_usuario_by_id(self, id_usuario):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id_usuario, nombre, email, password FROM usuarios WHERE id_usuario=%s",
                (id_usuario,),
            )
            return cur.fetchone()

    def get_usuario_by_email(self, email):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id_usuario, nombre, email, password FROM usuarios WHERE email=%s",
                (email,),
            )
            return cur.fetchone()

    def get_cliente_by_cedula(self, cedula):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id_cliente, cedula, nombres, telefono, email, direccion FROM clientes WHERE cedula=%s",
                (cedula,),
            )
            return cur.fetchone()

    def get_producto_by_nombre(self, nombre):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id_producto, nombre, categoria, cantidad, precio FROM productos_mysql WHERE nombre=%s LIMIT 1",
                (nombre,),
            )
            return cur.fetchone()

    def ensure_cliente(self, cedula, nombres, telefono='', email='', direccion=''):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id_cliente FROM clientes WHERE cedula=%s", (cedula,))
            row = cur.fetchone()
            if row:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE clientes SET nombres=%s, telefono=%s, email=%s, direccion=%s WHERE id_cliente=%s",
                    (nombres, telefono, email, direccion, row['id_cliente']),
                )
                conn.commit()
                return row['id_cliente']

            cur = conn.cursor()
            cur.execute(
                "INSERT INTO clientes (cedula, nombres, telefono, email, direccion) VALUES (%s, %s, %s, %s, %s)",
                (cedula, nombres, telefono, email, direccion),
            )
            conn.commit()
            return cur.lastrowid

    def ensure_producto_mysql(self, nombre, categoria, cantidad, precio):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id_producto FROM productos_mysql WHERE nombre=%s LIMIT 1",
                (nombre,),
            )
            row = cur.fetchone()
            if row:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE productos_mysql SET categoria=%s, cantidad=%s, precio=%s WHERE id_producto=%s",
                    (categoria, cantidad, precio, row['id_producto']),
                )
                conn.commit()
                return row['id_producto']

            cur = conn.cursor()
            cur.execute(
                "INSERT INTO productos_mysql (nombre, categoria, cantidad, precio) VALUES (%s, %s, %s, %s)",
                (nombre, categoria, cantidad, precio),
            )
            conn.commit()
            return cur.lastrowid

    def sync_menu_productos(self, productos):
        synced_ids = []
        for producto in productos:
            synced_ids.append(
                self.ensure_producto_mysql(
                    producto.get('nombre', ''),
                    producto.get('categoria', ''),
                    int(producto.get('cantidad') or 0),
                    float(producto.get('precio') or 0),
                )
            )
        return synced_ids

    def crear_pedido(self, usuario, items, metodo_pago='Efectivo', detalle_pago=None):
        if not items:
            raise ValueError('El pedido no contiene productos.')

        cedula = f"USR-{usuario.id_usuario}"
        id_cliente = self.ensure_cliente(cedula, usuario.nombre, email=usuario.email)

        subtotal = round(sum(float(item['precio']) * int(item['cantidad']) for item in items), 2)
        iva = round(subtotal * 0.15, 2)
        total = round(subtotal + iva, 2)

        detalle_pago_json = json.dumps(detalle_pago or {}, ensure_ascii=True)

        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO facturas (id_cliente, subtotal, iva, total, metodo_pago, detalle_pago) VALUES (%s, %s, %s, %s, %s, %s)",
                (id_cliente, subtotal, iva, total, metodo_pago, detalle_pago_json),
            )
            id_factura = cur.lastrowid

            for item in items:
                cur.execute(
                    "INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio_unitario) VALUES (%s, %s, %s, %s)",
                    (id_factura, item['id_producto'], int(item['cantidad']), float(item['precio'])),
                )

            conn.commit()

        return {
            'id_factura': id_factura,
            'subtotal': subtotal,
            'iva': iva,
            'total': total,
            'metodo_pago': metodo_pago,
            'detalle_pago': detalle_pago or {},
        }

    def delete_usuario(self, id_usuario):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
            conn.commit()

    def insert_producto(self, nombre, categoria, cantidad, precio):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO productos_mysql (nombre, categoria, cantidad, precio) VALUES (%s, %s, %s, %s)",
                (nombre, categoria, cantidad, precio),
            )
            conn.commit()

    def update_producto(self, id_producto, nombre, categoria, cantidad, precio):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE productos_mysql SET nombre=%s, categoria=%s, cantidad=%s, precio=%s WHERE id_producto=%s",
                (nombre, categoria, cantidad, precio, id_producto),
            )
            conn.commit()

    def delete_producto(self, id_producto):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM productos_mysql WHERE id_producto=%s", (id_producto,))
            conn.commit()

    def insert_reserva(self, cliente, telefono, email, personas, fecha_reserva):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO reservas_mysql (cliente, telefono, email, personas, fecha_reserva) VALUES (%s, %s, %s, %s, %s)",
                (cliente, telefono, email, personas, fecha_reserva),
            )
            conn.commit()

    def update_reserva(self, id_reserva, cliente, telefono, email, personas, fecha_reserva):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE reservas_mysql SET cliente=%s, telefono=%s, email=%s, personas=%s, fecha_reserva=%s WHERE id_reserva=%s",
                (cliente, telefono, email, personas, fecha_reserva, id_reserva),
            )
            conn.commit()

    def delete_reserva(self, id_reserva):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM reservas_mysql WHERE id_reserva=%s", (id_reserva,))
            conn.commit()

    def insert_usuario_trabajo(self, nombre_completo, nombre_usuario, correo, telefono, password, cargo_interes):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO usuarios_trabajo
                   (nombre_completo, nombre_usuario, correo, telefono, password, cargo_interes)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (nombre_completo, nombre_usuario, correo, telefono, password, cargo_interes),
            )
            conn.commit()

    def get_usuarios_trabajo(self, limit=12):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """SELECT nombre_completo, nombre_usuario, correo, telefono, cargo_interes, fecha_registro
                   FROM usuarios_trabajo ORDER BY id DESC LIMIT %s""",
                (limit,),
            )
            return cur.fetchall()
