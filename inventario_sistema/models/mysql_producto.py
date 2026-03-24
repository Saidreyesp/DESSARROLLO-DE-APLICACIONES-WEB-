from dataclasses import dataclass
from decimal import Decimal


@dataclass
class MySQLProducto:
    id_producto: int
    nombre: str
    categoria: str
    cantidad: int
    precio: Decimal

    @classmethod
    def from_row(cls, row: dict):
        return cls(
            id_producto=int(row.get("id_producto", 0)),
            nombre=str(row.get("nombre", "")),
            categoria=str(row.get("categoria") or ""),
            cantidad=int(row.get("cantidad", 0)),
            precio=Decimal(str(row.get("precio", 0))),
        )

    @property
    def valor_total(self) -> Decimal:
        return self.precio * self.cantidad
