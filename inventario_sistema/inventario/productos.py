from inventario.bd import db
from datetime import datetime


class Producto(db.Model):
    """
    Modelo de Producto para SQLAlchemy.
    
    Representa un producto en el sistema de inventario con todos sus atributos
    incluyendo información de auditoría (fechas de creación y actualización).
    """
    
    __tablename__ = 'producto'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    precio = db.Column(db.Float, default=0.0, nullable=False)
    cantidad = db.Column(db.Integer, default=0, nullable=False)
    categoria = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(500))  # URL de la imagen del plato
    fecha_creacion = db.Column(db.DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Producto {self.id}: {self.nombre}>"
    
    def to_dict(self):
        """Convierte el objeto Producto a diccionario."""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'categoria': self.categoria,
            'descripcion': self.descripcion,
            'imagen': self.imagen,
            'fecha_creacion': self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if self.fecha_actualizacion else None,
            'valor_total': self.precio * self.cantidad
        }
