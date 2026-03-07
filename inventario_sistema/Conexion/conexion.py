import os
from contextlib import contextmanager


class MySQLManager:
    """Gestiona conexion, creacion de tablas y operaciones CRUD en MySQL."""

    def __init__(self):
        self.host = os.getenv("MYSQL_HOST", "127.0.0.1")
        self.user = os.getenv("MYSQL_USER", "root")
        self.password = os.getenv("MYSQL_PASSWORD", "")
        self.database = os.getenv("MYSQL_DATABASE", "comedor_alexandra")
        self.port = int(os.getenv("MYSQL_PORT", "3306"))

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
            raise RuntimeError("mysql-connector-python no esta instalado.")

        conn = connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
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
                mail VARCHAR(150) NOT NULL UNIQUE,
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
                personas INT NOT NULL DEFAULT 1,
                fecha_reserva DATETIME,
                creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
        ]

        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            for q in queries:
                cur.execute(q)
            conn.commit()

    def fetch_all(self, table_name, id_column):
        with self.connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(f"SELECT * FROM {table_name} ORDER BY {id_column} DESC")
            return cur.fetchall()

    def insert_usuario(self, nombre, mail, password):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
                (nombre, mail, password),
            )
            conn.commit()

    def update_usuario(self, id_usuario, nombre, mail, password):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE usuarios SET nombre=%s, mail=%s, password=%s WHERE id_usuario=%s",
                (nombre, mail, password, id_usuario),
            )
            conn.commit()

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

    def insert_reserva(self, cliente, telefono, personas, fecha_reserva):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO reservas_mysql (cliente, telefono, personas, fecha_reserva) VALUES (%s, %s, %s, %s)",
                (cliente, telefono, personas, fecha_reserva),
            )
            conn.commit()

    def update_reserva(self, id_reserva, cliente, telefono, personas, fecha_reserva):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE reservas_mysql SET cliente=%s, telefono=%s, personas=%s, fecha_reserva=%s WHERE id_reserva=%s",
                (cliente, telefono, personas, fecha_reserva, id_reserva),
            )
            conn.commit()

    def delete_reserva(self, id_reserva):
        with self.connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM reservas_mysql WHERE id_reserva=%s", (id_reserva,))
            conn.commit()
