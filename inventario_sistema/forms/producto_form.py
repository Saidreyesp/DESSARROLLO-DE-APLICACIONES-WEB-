from decimal import Decimal, InvalidOperation


class ProductoForm:
    def __init__(self, data: dict):
        self.data = data
        self.errors = []

    def validate(self) -> bool:
        self.errors.clear()

        nombre = (self.data.get("nombre") or "").strip()
        categoria = (self.data.get("categoria") or "").strip()
        cantidad_raw = (self.data.get("cantidad") or "0").strip()
        precio_raw = (self.data.get("precio") or "0").strip()

        if not nombre:
            self.errors.append("El nombre es obligatorio.")

        if len(nombre) > 120:
            self.errors.append("El nombre no puede superar 120 caracteres.")

        if categoria and len(categoria) > 80:
            self.errors.append("La categoria no puede superar 80 caracteres.")

        try:
            cantidad = int(cantidad_raw)
            if cantidad < 0:
                self.errors.append("La cantidad no puede ser negativa.")
        except ValueError:
            self.errors.append("La cantidad debe ser un numero entero.")

        try:
            precio = Decimal(precio_raw)
            if precio < 0:
                self.errors.append("El precio no puede ser negativo.")
        except (InvalidOperation, ValueError):
            self.errors.append("El precio debe ser un numero valido.")

        return len(self.errors) == 0

    def cleaned_data(self) -> dict:
        return {
            "nombre": (self.data.get("nombre") or "").strip(),
            "categoria": (self.data.get("categoria") or "").strip(),
            "cantidad": int((self.data.get("cantidad") or "0").strip()),
            "precio": float((self.data.get("precio") or "0").strip()),
        }
