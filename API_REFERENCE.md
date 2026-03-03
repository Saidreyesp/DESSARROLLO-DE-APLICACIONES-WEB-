# API de GestorInventario - Documentación Completa

## Introducción

`GestorInventario` es una clase utilitaria que proporciona una interfaz de alto nivel para gestionar la persistencia de datos en múltiples formatos (SQLite, JSON, CSV, TXT).

## Instalación y Importación

```python
from inventario import GestorInventario, Producto, db
```

## Métodos Estáticos

### 1. Crear Productos

#### `crear_producto(nombre, precio=0.0, cantidad=0, categoria=None, descripcion=None)`

Crea un nuevo producto y lo persiste en todas las fuentes.

**Parámetros:**
- `nombre` (str): Nombre del producto (requerido, único)
- `precio` (float): Precio unitario (default: 0.0)
- `cantidad` (int): Cantidad disponible (default: 0)
- `categoria` (str, optional): Categoría del producto
- `descripcion` (str, optional): Descripción del producto

**Returns:** `Producto` si es exitoso, `None` si hay error

**Ejemplo:**
```python
producto = GestorInventario.crear_producto(
    nombre="Ceviche",
    precio=12.50,
    cantidad=8,
    categoria="Mariscos",
    descripcion="Ceviche ecuatoriano fresco"
)

if producto:
    print(f"Producto creado: {producto.nombre} (ID: {producto.id})")
```

### 2. Obtener Productos

#### `obtener_todos()`

Obtiene todos los productos de la base de datos.

**Returns:** Lista de objetos `Producto`

**Ejemplo:**
```python
productos = GestorInventario.obtener_todos()
for p in productos:
    print(f"{p.nombre}: ${p.precio} x {p.cantidad} unidades")
```

#### `obtener_por_id(producto_id)`

Obtiene un producto por su ID.

**Parámetros:**
- `producto_id` (int): ID del producto

**Returns:** Objeto `Producto` o `None` si no existe

**Ejemplo:**
```python
producto = GestorInventario.obtener_por_id(1)
if producto:
    print(f"Encontrado: {producto.nombre}")
```

#### `obtener_por_nombre(nombre)`

Obtiene un producto por su nombre.

**Parámetros:**
- `nombre` (str): Nombre del producto

**Returns:** Objeto `Producto` o `None` si no existe

**Ejemplo:**
```python
producto = GestorInventario.obtener_por_nombre("Locro")
if producto:
    print(f"ID: {producto.id}, Precio: ${producto.precio}")
```

#### `obtener_por_categoria(categoria)`

Obtiene todos los productos de una categoría.

**Parámetros:**
- `categoria` (str): Nombre de la categoría

**Returns:** Lista de objetos `Producto`

**Ejemplo:**
```python
mariscos = GestorInventario.obtener_por_categoria("Mariscos")
print(f"Productos de mariscos: {len(mariscos)}")
```

#### `obtener_bajo_stock(cantidad_minima=5)`

Obtiene productos con stock menor al especificado.

**Parámetros:**
- `cantidad_minima` (int): Cantidad mínima (default: 5)

**Returns:** Lista de objetos `Producto`

**Ejemplo:**
```python
bajo_stock = GestorInventario.obtener_bajo_stock(cantidad_minima=10)
for p in bajo_stock:
    print(f"⚠️  {p.nombre}: {p.cantidad} unidades")
```

### 3. Actualizar Productos

#### `actualizar_producto(producto_id, **kwargs)`

Actualiza los datos de un producto existente.

**Parámetros:**
- `producto_id` (int): ID del producto
- `**kwargs`: Campos a actualizar (nombre, precio, cantidad, categoria, descripcion)

**Returns:** Objeto `Producto` actualizado, `None` si hay error

**Ejemplo:**
```python
producto_actualizado = GestorInventario.actualizar_producto(
    1,
    nombre="Ceviche Mixto",
    precio=14.00,
    cantidad=12
)

if producto_actualizado:
    print(f"✓ Actualizado: {producto_actualizado.nombre}")
```

### 4. Eliminar Productos

#### `eliminar_producto(producto_id)`

Elimina un producto de la base de datos.

**Parámetros:**
- `producto_id` (int): ID del producto

**Returns:** `True` si es exitoso, `False` si hay error

**Ejemplo:**
```python
if GestorInventario.eliminar_producto(1):
    print("✓ Producto eliminado")
else:
    print("✗ Error al eliminar producto")
```

### 5. Reportes y Análisis

#### `obtener_estadisticas()`

Obtiene estadísticas generales del inventario.

**Returns:** Diccionario con estadísticas

**Estructura del retorno:**
```python
{
    'total_productos': int,           # Cantidad de productos
    'total_cantidad': int,            # Cantidad total de unidades
    'valor_total': float,             # Valor monetario total
    'precio_promedio': float,         # Precio promedio
    'producto_mas_caro': Producto,    # Producto con mayor precio
    'producto_mas_barato': Producto,  # Producto con menor precio
    'productos_bajo_stock': int       # Cantidad de productos bajo stock
}
```

**Ejemplo:**
```python
stats = GestorInventario.obtener_estadisticas()

print(f"Total de productos: {stats['total_productos']}")
print(f"Valor total: ${stats['valor_total']:.2f}")
print(f"Precio promedio: ${stats['precio_promedio']:.2f}")
print(f"Producto más caro: {stats['producto_mas_caro'].nombre}")
```

#### `obtener_datos_multiples_fuentes()`

Obtiene datos de todas las fuentes de persistencia.

**Returns:** Diccionario con listas de datos

**Estructura del retorno:**
```python
{
    'sqlite': [dict, ...],   # Datos de base de datos
    'txt': [dict, ...],      # Datos de archivo TXT
    'json': [dict, ...],     # Datos de archivo JSON
    'csv': [dict, ...]       # Datos de archivo CSV
}
```

**Ejemplo:**
```python
datos = GestorInventario.obtener_datos_multiples_fuentes()

print(f"SQLite: {len(datos['sqlite'])} registros")
print(f"JSON: {len(datos['json'])} registros")
print(f"CSV: {len(datos['csv'])} registros")
print(f"TXT: {len(datos['txt'])} registros")
```

### 6. Validación

#### `validar_producto(nombre, precio, cantidad)`

Valida los datos de un producto.

**Parámetros:**
- `nombre` (str): Nombre del producto
- `precio` (float): Precio unitario
- `cantidad` (int o float): Cantidad

**Returns:** Tupla `(es_valido: bool, mensaje: str)`

**Ejemplo:**
```python
es_valido, mensaje = GestorInventario.validar_producto("Ceviche", 12.50, 8)

if es_valido:
    print("✓ Validación correcta")
    # Crear producto
else:
    print(f"✗ Error: {mensaje}")
```

**Validaciones realizadas:**
- ✅ Nombre debe ser string no vacío
- ✅ Precio debe ser número positivo (>= 0)
- ✅ Cantidad debe ser número positivo (>= 0)

## Modelos de Datos

### Clase Producto

```python
class Producto(db.Model):
    id: int                    # Clave primaria
    nombre: str               # Nombre (único)
    precio: float             # Precio unitario
    cantidad: int             # Cantidad disponible
    categoria: str            # Categoría
    descripcion: str          # Descripción
    fecha_creacion: datetime  # Fecha de creación
    fecha_actualizacion: datetime  # Última actualización
```

#### Métodos de Producto

##### `to_dict()`

Convierte el objeto Producto a diccionario.

**Returns:** Diccionario con todos los campos

**Ejemplo:**
```python
producto = GestorInventario.obtener_por_id(1)
dict_producto = producto.to_dict()

print(dict_producto)
# {
#     'id': 1,
#     'nombre': 'Ceviche',
#     'precio': 12.50,
#     'cantidad': 8,
#     'categoria': 'Mariscos',
#     'descripcion': 'Ceviche ecuatoriano fresco',
#     'fecha_creacion': '2026-03-02 10:30:45',
#     'fecha_actualizacion': '2026-03-02 10:30:45',
#     'valor_total': 100.0
# }
```

## Funciones de Persistencia

Estas funciones están en el módulo `inventario.persistencia`:

### TXT (Texto Plano)

```python
from inventario import save_txt, read_txt

# Guardar
save_txt({'id': 1, 'nombre': 'Ceviche', 'precio': 12.50})

# Leer
datos = read_txt()  # Retorna lista de diccionarios
```

### JSON

```python
from inventario import save_json, read_json

# Guardar (agrega al archivo)
save_json({'nombre': 'Locro', 'precio': 7.50})

# Leer
datos = read_json()  # Retorna lista de diccionarios
```

### CSV

```python
from inventario import save_csv, read_csv

# Guardar (agrega al archivo)
save_csv({'nombre': 'Lomo', 'precio': 15.00, 'cantidad': 5})

# Leer
datos = read_csv()  # Retorna lista de diccionarios
```

### SQLite (SQLAlchemy)

```python
from inventario import Producto, db

# Crear
nuevo = Producto(nombre="Test", precio=5.00, cantidad=10)
db.session.add(nuevo)
db.session.commit()

# Leer
todos = Producto.query.all()
uno = Producto.query.get(1)

# Actualizar
uno.cantidad = 15
db.session.commit()

# Eliminar
db.session.delete(uno)
db.session.commit()
```

## Casos de Uso Comunes

### Crear un producto y verificarlo

```python
# Validar primero
es_valido, msg = GestorInventario.validar_producto("Pizza", 5.00, 20)
if not es_valido:
    print(f"Error: {msg}")
    exit()

# Crear
producto = GestorInventario.crear_producto(
    nombre="Pizza",
    precio=5.00,
    cantidad=20,
    categoria="Pizzas"
)

if producto:
    print(f"✓ Creado: {producto.nombre}")
else:
    print("✗ No se pudo crear")
```

### Actualizar stock después de una venta

```python
producto = GestorInventario.obtener_por_nombre("Ceviche")
if producto:
    nueva_cantidad = producto.cantidad - 1  # Una unidad vendida
    GestorInventario.actualizar_producto(
        producto.id,
        cantidad=nueva_cantidad
    )
    print(f"✓ Stock actualizado: {nueva_cantidad} unidades")
```

### Generar reporte de bajo stock

```python
bajo_stock = GestorInventario.obtener_bajo_stock(cantidad_minima=5)
print("Productos que necesitan reabastecimiento:")
for p in bajo_stock:
    print(f"  - {p.nombre}: {p.cantidad} unidades")
```

### Exportar datos a JSON

```python
datos = GestorInventario.obtener_datos_multiples_fuentes()
import json

with open('exportar.json', 'w') as f:
    json.dump(datos['sqlite'], f, indent=2)
print("✓ Datos exportados a exportar.json")
```

## Manejo de Errores

```python
try:
    producto = GestorInventario.crear_producto("Ceviche", 12.50, 8)
    if not producto:
        print("Error desconocido al crear producto")
except Exception as e:
    print(f"Error: {e}")

# Validar antes de actualizar
if GestorInventario.obtener_por_id(999):
    GestorInventario.actualizar_producto(999, precio=10.00)
else:
    print("Producto no existe")
```

## Sincronización Automática

Cuando usas `GestorInventario.crear_producto()`, automáticamente:
1. ✅ Guarda en SQLite
2. ✅ Guarda en JSON
3. ✅ Guarda en CSV
4. ✅ Guarda en TXT

No necesitas llamar a las funciones de persistencia directamente.

## Performance

- `obtener_todos()`: O(n) - puede ser lento con muchos registros
- `obtener_por_id()`: O(1) - muy rápido
- `obtener_por_nombre()`: O(n) - busca lineal
- `obtener_por_categoria()`: O(n) - busca lineal
- `obtener_bajo_stock()`: O(n) - requiere filtrado

## Mejores Prácticas

1. ✅ Siempre valida datos antes de guardar
2. ✅ Verifica si el producto existe antes de actualizar
3. ✅ Maneja excepciones apropiadamente
4. ✅ Usa `obtener_por_id()` en lugar de `obtener_todos()` cuando sea posible
5. ✅ Sincroniza datos regularmente entre fuentes
6. ✅ Mantén backups de la base de datos

## Soporte

Para reportar bugs o solicitar features, contacta al equipo de desarrollo.

---

**Última actualización:** Marzo 2026  
**Versión:** 1.0 - Semana 12
