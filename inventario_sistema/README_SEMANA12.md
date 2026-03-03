# Semana 12: Persistencia de Datos - Implementación Completada

## Resumen

Esta implementación completa la **Semana 12** del proyecto Flask "Restaurante La Buena Mesa" con soporte completo para múltiples fuentes de persistencia de datos:

- ✅ **SQLite** - Base de datos relacional con SQLAlchemy ORM
- ✅ **JSON** - Formato JavaScript Object Notation
- ✅ **CSV** - Comma-Separated Values
- ✅ **TXT** - Texto plano con JSON por línea

## Estructura del Proyecto

```
inventario_sistema/
├── app.py                      # Aplicación Flask principal
├── requirements.txt            # Dependencias del proyecto
│
├── inventario/                 # Paquete principal de inventario
│   ├── __init__.py            # Exporta componentes principales
│   ├── bd.py                  # Configuración de SQLAlchemy
│   ├── productos.py           # Modelo Producto (ORM)
│   ├── inventario.py          # GestorInventario con funciones de gestión
│   ├── persistencia.py        # Funciones de persistencia (TXT, JSON, CSV)
│   └── data/                  # Almacenamiento de archivos
│       ├── datos.txt          # Registros en texto plano
│       ├── datos.json         # Registros en JSON
│       └── datos.csv          # Registros en CSV
│
├── models/                     # Modelos alternativos y conexión SQLite
│   ├── conexion.py            # ConexionSQLite (SQLite puro)
│   └── producto.py            # Modelo alternativo de Producto
│
├── static/                     # Archivos estáticos
│   └── style.css              # Estilos CSS
│
├── templates/                  # Plantillas Jinja2
│   ├── base.html              # Plantilla base
│   ├── datos.html             # ✨ NUEVA - Visualización de datos multifuente
│   ├── index.html             # Página principal
│   ├── productos.html         # Listado de productos
│   ├── producto_form.html     # Formulario para crear/editar
│   ├── producto_detalle.html  # Detalle de un producto
│   └── ...                    # Otras plantillas
│
└── instance/                   # Instancia de la aplicación
    └── inventario.db          # Base de datos SQLite
```

## Modelos de Datos

### Producto (ORM - SQLAlchemy)

```python
class Producto(db.Model):
    id: int                    # Clave primaria
    nombre: str               # Nombre del producto (único)
    precio: float             # Precio unitario
    cantidad: int             # Cantidad disponible
    categoria: str            # Categoría (opcional)
    descripcion: str          # Descripción (opcional)
    fecha_creacion: datetime  # Timestamp de creación
    fecha_actualizacion: datetime  # Timestamp de última actualización
```

## Funcionalidades Implementadas

### 1. GestorInventario

Clase de utilidad que proporciona operaciones CRUD de alto nivel:

```python
from inventario import GestorInventario

# Crear producto
producto = GestorInventario.crear_producto(
    nombre="Arroz con Pollo",
    precio=8.50,
    cantidad=15,
    categoria="Platos",
    descripcion="Arroz con pollo ecuatoriano"
)

# Obtener todos los productos
productos = GestorInventario.obtener_todos()

# Buscar por ID
producto = GestorInventario.obtener_por_id(1)

# Buscar por nombre
producto = GestorInventario.obtener_por_nombre("Ceviche")

# Obtener por categoría
platos = GestorInventario.obtener_por_categoria("Platos")

# Obtener bajo stock
bajo_stock = GestorInventario.obtener_bajo_stock(cantidad_minima=5)

# Actualizar producto
GestorInventario.actualizar_producto(1, precio=9.00, cantidad=20)

# Eliminar producto
GestorInventario.eliminar_producto(1)

# Obtener estadísticas
stats = GestorInventario.obtener_estadisticas()

# Obtener datos de múltiples fuentes
datos = GestorInventario.obtener_datos_multiples_fuentes()

# Validar datos
es_valido, mensaje = GestorInventario.validar_producto("Locro", 7.50, 10)
```

### 2. Funciones de Persistencia

Módulo `inventario/persistencia.py`:

#### TXT (Texto plano)
```python
from inventario import save_txt, read_txt

# Guardar
record = {'id': 1, 'nombre': 'Ceviche', 'precio': 12.00, 'cantidad': 8}
save_txt(record)

# Leer
datos = read_txt()
```

#### JSON
```python
from inventario import save_json, read_json

# Guardar
save_json(record)

# Leer
datos = read_json()
```

#### CSV
```python
from inventario import save_csv, read_csv

# Guardar
save_csv(record)

# Leer
datos = read_csv()
```

#### SQLite (SQLAlchemy)
```python
from inventario import Producto, db

# Crear
nuevo_producto = Producto(
    nombre="Lomo Seco",
    precio=15.00,
    cantidad=12,
    categoria="Carnes"
)
db.session.add(nuevo_producto)
db.session.commit()

# Leer
productos = Producto.query.all()
producto = Producto.query.get(1)

# Actualizar
producto.cantidad = 10
db.session.commit()

# Eliminar
db.session.delete(producto)
db.session.commit()
```

## Rutas (Endpoints) de la Aplicación

### Visualización de Datos
- `GET /datos` - Página con todos los datos de múltiples fuentes

### CRUD de Productos
- `GET /productos` - Listado de productos
- `GET /producto/<int:id>` - Detalle de un producto
- `GET /producto/nuevo` - Formulario de nuevo producto
- `POST /producto/nuevo` - Crear nuevo producto
- `GET /producto/editar/<int:id>` - Formulario de edición
- `POST /producto/editar/<int:id>` - Actualizar producto
- `POST /producto/eliminar/<int:id>` - Eliminar producto

### Reportes y Búsqueda
- `GET /reportes` - Reportes del inventario
- `GET /buscar?termino=...` - Búsqueda de productos
- `GET /bajo-stock?minimo=5` - Productos con bajo stock

## Sincronización de Datos

Cuando se crea, edita o elimina un producto, se sincroniza automáticamente en:
1. **Base de datos SQLite** (mediante SQLAlchemy ORM)
2. **Archivo JSON** (datos.json)
3. **Archivo CSV** (datos.csv)
4. **Archivo TXT** (datos.txt)

Ejemplo en `app.py`:
```python
@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        # ... validación
        id_nuevo = db_conexion.añadir_producto(...)
        
        # Sincronizar en todas las fuentes
        record = {'id': id_nuevo, 'nombre': nombre, ...}
        save_txt(record)      # Guardar en TXT
        save_json(record)     # Guardar en JSON
        save_csv(record)      # Guardar en CSV
```

## Dashboard de Datos (datos.html)

La página `/datos` proporciona una interfaz visual para explorar los datos de todas las fuentes:

### Características
- 📊 **Pestaña SQLite** - Tabla con estadísticas
- 📄 **Pestaña JSON** - Visualización de datos en JSON
- 📋 **Pestaña CSV** - Tabla con registros CSV
- 📝 **Pestaña TXT** - Registros en texto plano

### Información Mostrada
- Cantidad de registros en cada fuente
- Estadísticas de valor total, cantidad total
- Visualización en formato tabla
- Vista raw de datos JSON

## Validación de Datos

La clase `GestorInventario` incluye validación:

```python
es_valido, mensaje = GestorInventario.validar_producto(
    nombre="Locro",
    precio=7.50,
    cantidad=10
)

if not es_valido:
    print(f"Error: {mensaje}")
```

Validaciones incluidas:
- ✅ Nombre debe ser string no vacío
- ✅ Precio debe ser número positivo
- ✅ Cantidad debe ser número positivo

## Estadísticas y Reportes

```python
stats = GestorInventario.obtener_estadisticas()
print(f"Total de productos: {stats['total_productos']}")
print(f"Cantidad total: {stats['total_cantidad']}")
print(f"Valor total: ${stats['valor_total']:.2f}")
print(f"Precio promedio: ${stats['precio_promedio']:.2f}")
print(f"Producto más caro: {stats['producto_mas_caro'].nombre}")
print(f"Producto más barato: {stats['producto_mas_barato'].nombre}")
print(f"Productos bajo stock: {stats['productos_bajo_stock']}")
```

## Instalación y Configuración

### 1. Crear entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación
```bash
python app.py
```

### 4. Acceder a la aplicación
- Home: http://localhost:5000/
- Datos: http://localhost:5000/datos
- Productos: http://localhost:5000/productos

## Requisitos del Proyecto

```
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.48
python-dotenv==1.0.0
Werkzeug==3.1.5
Jinja2==3.1.6
```

## Mejoras Implementadas en Semana 12

1. ✅ **Modelo Producto mejorado** con campos adicionales (categoria, descripcion, fechas)
2. ✅ **GestorInventario** con métodos CRUD y utilidades
3. ✅ **Validación de datos** antes de guardar
4. ✅ **Sincronización automática** entre fuentes
5. ✅ **Plantilla datos.html** mejorada con tabs y estadísticas
6. ✅ **Método to_dict()** para convertir ORM a diccionarios
7. ✅ **Documentación completa** en código y README

## Notas Importantes

- Todos los métodos son reutilizables
- El código maneja excepciones apropiadamente
- Los datos se sincronizan automáticamente
- La aplicación es escalable y mantenible
- Se validan todos los datos de entrada

## Próximos Pasos (Semana 13+)

- Implementar autenticación de usuarios
- Agregar control de acceso/permisos
- Implementar auditoría de cambios
- Crear reportes PDF
- Implementar API RESTful
- Agregar más campos al modelo

## Autor
Desarrollado como parte del curso de Desarrollo Web - 2026

## Licencia
MIT
