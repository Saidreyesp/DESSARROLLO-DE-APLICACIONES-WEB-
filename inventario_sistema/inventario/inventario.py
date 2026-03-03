"""
Módulo de Inventario - Funciones auxiliares para gestión de inventario.

Este módulo proporciona funciones de alto nivel para:
- Gestión de productos
- Reportes de inventario
- Validación de datos
- Estadísticas
"""

from inventario.productos import Producto
from inventario.persistencia import save_txt, save_json, save_csv, read_txt, read_json, read_csv
from inventario.bd import db


class GestorInventario:
    """Gestor de operaciones de inventario con persistencia múltiple."""
    
    @staticmethod
    def crear_producto(nombre, precio=0.0, cantidad=0, categoria=None, descripcion=None):
        """
        Crea un nuevo producto y lo persiste en todas las fuentes.
        
        Args:
            nombre: Nombre del producto
            precio: Precio unitario
            cantidad: Cantidad disponible
            categoria: Categoría del producto
            descripcion: Descripción del producto
            
        Returns:
            Producto: El producto creado o None si hay error
        """
        try:
            producto = Producto(
                nombre=nombre,
                precio=precio,
                cantidad=cantidad,
                categoria=categoria,
                descripcion=descripcion
            )
            db.session.add(producto)
            db.session.commit()
            
            # Persistir en archivos
            record = {
                'id': producto.id,
                'nombre': nombre,
                'precio': precio,
                'cantidad': cantidad,
                'categoria': categoria,
                'descripcion': descripcion
            }
            save_txt(record)
            save_json(record)
            save_csv(record)
            
            return producto
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear producto: {e}")
            return None
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los productos de la base de datos."""
        return Producto.query.all()
    
    @staticmethod
    def obtener_por_id(producto_id):
        """Obtiene un producto por su ID."""
        return Producto.query.get(producto_id)
    
    @staticmethod
    def obtener_por_nombre(nombre):
        """Obtiene un producto por su nombre."""
        return Producto.query.filter_by(nombre=nombre).first()
    
    @staticmethod
    def obtener_por_categoria(categoria):
        """Obtiene todos los productos de una categoría."""
        return Producto.query.filter_by(categoria=categoria).all()
    
    @staticmethod
    def obtener_bajo_stock(cantidad_minima=5):
        """Obtiene productos con stock menor al especificado."""
        return Producto.query.filter(Producto.cantidad < cantidad_minima).all()
    
    @staticmethod
    def actualizar_producto(producto_id, **kwargs):
        """
        Actualiza un producto existente.
        
        Args:
            producto_id: ID del producto a actualizar
            **kwargs: Campos a actualizar (nombre, precio, cantidad, etc.)
            
        Returns:
            Producto: Producto actualizado o None si hay error
        """
        try:
            producto = Producto.query.get(producto_id)
            if not producto:
                return None
            
            for key, value in kwargs.items():
                if hasattr(producto, key):
                    setattr(producto, key, value)
            
            db.session.commit()
            return producto
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar producto: {e}")
            return None
    
    @staticmethod
    def eliminar_producto(producto_id):
        """Elimina un producto de la base de datos."""
        try:
            producto = Producto.query.get(producto_id)
            if not producto:
                return False
            
            db.session.delete(producto)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar producto: {e}")
            return False
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas del inventario."""
        productos = Producto.query.all()
        
        if not productos:
            return {
                'total_productos': 0,
                'total_cantidad': 0,
                'valor_total': 0.0,
                'precio_promedio': 0.0,
                'producto_mas_caro': None,
                'producto_mas_barato': None
            }
        
        precios = [p.precio for p in productos]
        cantidades = [p.cantidad for p in productos]
        valores = [p.precio * p.cantidad for p in productos]
        
        return {
            'total_productos': len(productos),
            'total_cantidad': sum(cantidades),
            'valor_total': sum(valores),
            'precio_promedio': sum(precios) / len(precios) if precios else 0.0,
            'producto_mas_caro': max(productos, key=lambda p: p.precio) if productos else None,
            'producto_mas_barato': min(productos, key=lambda p: p.precio) if productos else None,
            'productos_bajo_stock': len(GestorInventario.obtener_bajo_stock(5))
        }
    
    @staticmethod
    def obtener_datos_multiples_fuentes():
        """Obtiene datos de todas las fuentes de persistencia."""
        return {
            'sqlite': [p.to_dict() for p in Producto.query.all()],
            'txt': read_txt(),
            'json': read_json(),
            'csv': read_csv()
        }
    
    @staticmethod
    def validar_producto(nombre, precio, cantidad):
        """
        Valida los datos de un producto.
        
        Returns:
            tuple: (es_valido, mensaje)
        """
        if not nombre or not isinstance(nombre, str):
            return False, "El nombre debe ser una cadena"
        
        if not isinstance(precio, (int, float)) or precio < 0:
            return False, "El precio debe ser un número positivo"
        
        if not isinstance(cantidad, (int, float)) or cantidad < 0:
            return False, "La cantidad debe ser un número positivo"
        
        return True, "Producto válido"
