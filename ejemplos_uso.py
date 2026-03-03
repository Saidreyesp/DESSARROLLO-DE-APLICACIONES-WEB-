"""
Ejemplos de uso de GestorInventario - Semana 12

Este archivo muestra cómo utilizar las funcionalidades del sistema de inventario
con múltiples fuentes de persistencia de datos.
"""

from inventario import GestorInventario, Producto, db

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def ejemplo_crear_productos():
    """Ejemplo: Crear productos usando GestorInventario."""
    print("\n=== Creando Productos ===")
    
    productos_datos = [
        {
            'nombre': 'Ceviche',
            'precio': 12.50,
            'cantidad': 8,
            'categoria': 'Mariscos',
            'descripcion': 'Ceviche ecuatoriano fresco'
        },
        {
            'nombre': 'Locro',
            'precio': 7.50,
            'cantidad': 15,
            'categoria': 'Sopas',
            'descripcion': 'Locro de papa y queso'
        },
        {
            'nombre': 'Lomo Seco',
            'precio': 15.00,
            'cantidad': 5,
            'categoria': 'Carnes',
            'descripcion': 'Carne seca con papas y aguacate'
        }
    ]
    
    for datos in productos_datos:
        producto = GestorInventario.crear_producto(**datos)
        if producto:
            print(f"✓ Producto '{producto.nombre}' creado con ID {producto.id}")
        else:
            print(f"✗ Error al crear '{datos['nombre']}'")


def ejemplo_obtener_productos():
    """Ejemplo: Obtener productos de diferentes formas."""
    print("\n=== Obteniendo Productos ===")
    
    # Obtener todos
    todos = GestorInventario.obtener_todos()
    print(f"\nTotal de productos: {len(todos)}")
    for p in todos:
        print(f"  - {p.nombre}: ${p.precio} x {p.cantidad} unidades")
    
    # Obtener por ID
    producto = GestorInventario.obtener_por_id(1)
    if producto:
        print(f"\nProducto ID 1: {producto.nombre}")
    
    # Obtener por nombre
    producto = GestorInventario.obtener_por_nombre('Ceviche')
    if producto:
        print(f"Producto encontrado: {producto.nombre} - ${producto.precio}")
    
    # Obtener por categoría
    mariscos = GestorInventario.obtener_por_categoria('Mariscos')
    print(f"\nProductos en 'Mariscos': {len(mariscos)}")
    for p in mariscos:
        print(f"  - {p.nombre}: {p.cantidad} unidades")


def ejemplo_actualizar_producto():
    """Ejemplo: Actualizar datos de un producto."""
    print("\n=== Actualizando Productos ===")
    
    producto = GestorInventario.obtener_por_nombre('Ceviche')
    if producto:
        print(f"Antes: {producto.nombre} - ${producto.precio} x {producto.cantidad}")
        
        GestorInventario.actualizar_producto(
            producto.id,
            precio=13.50,
            cantidad=10
        )
        
        producto = GestorInventario.obtener_por_id(producto.id)
        print(f"Después: {producto.nombre} - ${producto.precio} x {producto.cantidad}")


def ejemplo_bajo_stock():
    """Ejemplo: Obtener productos con bajo stock."""
    print("\n=== Productos Bajo Stock ===")
    
    bajo_stock = GestorInventario.obtener_bajo_stock(cantidad_minima=10)
    print(f"Productos con menos de 10 unidades: {len(bajo_stock)}")
    
    for p in bajo_stock:
        print(f"  ⚠ {p.nombre}: {p.cantidad} unidades")


def ejemplo_estadisticas():
    """Ejemplo: Obtener estadísticas del inventario."""
    print("\n=== Estadísticas del Inventario ===")
    
    stats = GestorInventario.obtener_estadisticas()
    
    print(f"Total de productos: {stats['total_productos']}")
    print(f"Cantidad total en inventario: {stats['total_cantidad']} unidades")
    print(f"Valor total del inventario: ${stats['valor_total']:.2f}")
    print(f"Precio promedio: ${stats['precio_promedio']:.2f}")
    
    if stats['producto_mas_caro']:
        print(f"Producto más caro: {stats['producto_mas_caro'].nombre} (${stats['producto_mas_caro'].precio})")
    
    if stats['producto_mas_barato']:
        print(f"Producto más barato: {stats['producto_mas_barato'].nombre} (${stats['producto_mas_barato'].precio})")
    
    print(f"Productos con bajo stock: {stats['productos_bajo_stock']}")


def ejemplo_multiples_fuentes():
    """Ejemplo: Obtener datos de múltiples fuentes de persistencia."""
    print("\n=== Datos de Múltiples Fuentes ===")
    
    datos = GestorInventario.obtener_datos_multiples_fuentes()
    
    print(f"SQLite: {len(datos['sqlite'])} registros")
    print(f"JSON: {len(datos['json'])} registros")
    print(f"CSV: {len(datos['csv'])} registros")
    print(f"TXT: {len(datos['txt'])} registros")


def ejemplo_validacion():
    """Ejemplo: Validar datos de productos."""
    print("\n=== Validación de Datos ===")
    
    casos_prueba = [
        ('Arroz con Pollo', 8.50, 15),  # Válido
        ('', 5.00, 10),                   # Nombre vacío
        ('Pizza', -5.00, 8),              # Precio negativo
        ('Hamburguesa', 3.50, -2),        # Cantidad negativa
    ]
    
    for nombre, precio, cantidad in casos_prueba:
        es_valido, mensaje = GestorInventario.validar_producto(nombre, precio, cantidad)
        estado = "✓" if es_valido else "✗"
        print(f"{estado} {nombre or 'Sin nombre'}: {mensaje}")


def ejemplo_convertir_a_dict():
    """Ejemplo: Convertir objetos Producto a diccionarios."""
    print("\n=== Conversión de ORM a Diccionarios ===")
    
    productos = GestorInventario.obtener_todos()
    
    if productos:
        producto = productos[0]
        dict_producto = producto.to_dict()
        print(f"Producto como diccionario:")
        for key, value in dict_producto.items():
            print(f"  {key}: {value}")


def ejemplo_eliminar_producto():
    """Ejemplo: Eliminar un producto."""
    print("\n=== Eliminando Producto ===")
    
    producto = GestorInventario.obtener_por_nombre('Pizza')
    if producto:
        if GestorInventario.eliminar_producto(producto.id):
            print(f"✓ Producto '{producto.nombre}' eliminado")
        else:
            print(f"✗ Error al eliminar '{producto.nombre}'")
    else:
        print("Producto no encontrado")


# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("EJEMPLOS DE USO - GestorInventario (Semana 12)")
    print("=" * 60)
    
    # Nota: Para ejecutar estos ejemplos, debes estar en el contexto de la aplicación Flask
    # from app import app, db
    # with app.app_context():
    #     ejemplo_crear_productos()
    #     ejemplo_obtener_productos()
    #     ejemplo_actualizar_producto()
    #     ejemplo_bajo_stock()
    #     ejemplo_estadisticas()
    #     ejemplo_multiples_fuentes()
    #     ejemplo_validacion()
    #     ejemplo_convertir_a_dict()
    
    print("\n✓ Descomenta las líneas en __main__ para ejecutar los ejemplos")
    print("=" * 60)
