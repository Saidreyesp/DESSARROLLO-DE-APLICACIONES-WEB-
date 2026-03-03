"""Modelo Producto para programación orientada a objetos (alternativo a ORM)"""


class Producto:
    """Clase Producto con métodos getters y setters."""
    
    def __init__(self, id, nombre, cantidad, precio, categoria=None, descripcion=None):
        """Inicializa un producto con atributos básicos."""
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
        self._categoria = categoria
        self._descripcion = descripcion
    
    def get_id(self):
        """Obtiene el ID del producto."""
        return self._id
    
    def get_nombre(self):
        """Obtiene el nombre del producto."""
        return self._nombre
    
    def set_nombre(self, nombre):
        """Establece el nombre del producto."""
        if nombre and isinstance(nombre, str):
            self._nombre = nombre
        else:
            raise ValueError("El nombre debe ser una cadena no vacía")
    
    def get_cantidad(self):
        """Obtiene la cantidad disponible."""
        return self._cantidad
    
    def set_cantidad(self, cantidad):
        """Establece la cantidad, validando que sea positiva."""
        if isinstance(cantidad, int) and cantidad >= 0:
            self._cantidad = cantidad
        else:
            raise ValueError("La cantidad debe ser un número positivo")
    
    def get_precio(self):
        """Obtiene el precio unitario."""
        return self._precio
    
    def set_precio(self, precio):
        """Establece el precio, validando que sea positivo."""
        if isinstance(precio, (int, float)) and precio >= 0:
            self._precio = precio
        else:
            raise ValueError("El precio debe ser un número positivo")
    
    def get_categoria(self):
        """Obtiene la categoría."""
        return self._categoria
    
    def set_categoria(self, categoria):
        """Establece la categoría."""
        self._categoria = categoria
    
    def get_descripcion(self):
        """Obtiene la descripción."""
        return self._descripcion
    
    def set_descripcion(self, descripcion):
        """Establece la descripción."""
        self._descripcion = descripcion
    
    def get_valor_total(self):
        """Calcula el valor total del producto (precio * cantidad)."""
        return self._precio * self._cantidad
    
    def __repr__(self):
        """Representación en string del objeto."""
        return f"Producto(ID={self._id}, Nombre='{self._nombre}', Precio=${self._precio}, Cantidad={self._cantidad})"
    
    def __str__(self):
        """String legible del producto."""
        return f"{self._nombre} - ${self._precio} x {self._cantidad} = ${self.get_valor_total():.2f}"
