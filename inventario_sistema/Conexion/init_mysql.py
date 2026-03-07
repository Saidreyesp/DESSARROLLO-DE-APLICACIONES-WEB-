"""Script para crear tablas MySQL desde el proyecto Flask."""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from Conexion.conexion import MySQLManager


def main():
    manager = MySQLManager()
    ok, msg = manager.ping()
    if not ok:
        print(f"No se pudo conectar a MySQL: {msg}")
        return

    schema_path = os.path.join(os.path.dirname(__file__), "schema_mysql.sql")
    if not os.path.exists(schema_path):
        print("No se encontro schema_mysql.sql")
        return

    with open(schema_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    with manager.connection() as conn:
        cur = conn.cursor()
        for _ in cur.execute(sql_script, multi=True):
            pass
        conn.commit()

    print("Script SQL ejecutado correctamente desde schema_mysql.sql")


if __name__ == "__main__":
    main()
