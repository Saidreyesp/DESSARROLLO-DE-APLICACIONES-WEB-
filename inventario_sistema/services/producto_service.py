from decimal import Decimal

from models.mysql_producto import MySQLProducto


class ProductoService:
    def __init__(self, mysql_manager):
        self.mysql_manager = mysql_manager

    def listar(self):
        rows = self.mysql_manager.fetch_all("productos_mysql", "id_producto")
        return [MySQLProducto.from_row(row) for row in rows]

    def obtener(self, id_producto: int):
        rows = self.mysql_manager.fetch_where(
            "productos_mysql",
            "id_producto = %s",
            (id_producto,),
            order_by="id_producto DESC",
            limit=1,
        )
        if not rows:
            return None
        return MySQLProducto.from_row(rows[0])

    def crear(self, nombre: str, categoria: str, cantidad: int, precio: float):
        self.mysql_manager.insert_producto(nombre, categoria, cantidad, precio)

    def actualizar(self, id_producto: int, nombre: str, categoria: str, cantidad: int, precio: float):
        self.mysql_manager.update_producto(id_producto, nombre, categoria, cantidad, precio)

    def eliminar(self, id_producto: int):
        self.mysql_manager.delete_producto(id_producto)

    def resumen(self):
        productos = self.listar()
        total_items = len(productos)
        total_stock = sum(p.cantidad for p in productos)
        total_valor = sum(p.valor_total for p in productos)
        return {
            "total_items": total_items,
            "total_stock": total_stock,
            "total_valor": Decimal(total_valor),
            "productos": productos,
        }
