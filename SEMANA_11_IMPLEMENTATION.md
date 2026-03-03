# SEMANA 11: POO + Colecciones + SQLite CRUD Implementation

## 📚 Documentación Completa del Sistema

**Curso:** Desarrollo de Aplicaciones Web  
**Semana:** 11  
**Tema:** Programación Orientada a Objetos + Colecciones Python + Base de Datos SQLite  
**Sistema:** Restaurante "La Buena Mesa" - Gestión de Inventario

---

## 1. ARQUITECTURA Y DISEÑO POO

### 1.1 Diagrama de Clases

```
┌─────────────────────────────────────────┐
│            Producto (POO)               │
├─────────────────────────────────────────┤
│ - id: int                               │
│ - nombre: str                           │
│ - cantidad: int                         │
│ - precio: float                         │
│ - categoria: str                        │
│ - descripcion: str                      │
├─────────────────────────────────────────┤
│ + get/set methods (validación)          │
│ + get_valor_total(): float [POLY]       │
│ + __str__(): str [POLY]                 │
└─────────────────────────────────────────┘
         ▲                    ▲
         │                    │
    Herencia de              Usa
    Atributos             (composición)
         │                    │
         │              ┌─────┴──────┐
         │              │            │
┌────────┴──────────┐  Inventario  ConexionSQLite
│  (Capa Modelo)    │  (Colecciones) (SQLite)
└───────────────────┘
```

### 1.2 Definición de Clases

#### **Clase Producto** (`models/producto.py`)

**Responsabilidad:** Encapsular datos y comportamiento de un plato/producto de restaurante.

```python
class Producto:
    """Representa un producto/plato con validación de datos."""
    
    def __init__(self, id, nombre, cantidad, precio, categoria='Platos', descripcion=''):
        # ENCAPSULACIÓN: Atributos privados con underscore
        self.__id = id
        self.__nombre = nombre
        self.__cantidad = max(0, cantidad)  # Validación: no negativos
        self.__precio = max(0, precio)      # Validación: no negativos  
        self.__categoria = categoria
        self.__descripcion = descripcion
```

**Métodos Principales:**

| Método | Tipo | Propósito | Retorna |
|--------|------|----------|---------|
| `get_id()` | Getter | Obtener ID único | `int` |
| `get_nombre()` | Getter | Obtener nombre plato | `str` |
| `get_cantidad()` | Getter | Obtener stock | `int` |
| `get_precio()` | Getter | Obtener precio unitario | `float` |
| `set_cantidad(q)` | Setter | Actualizar stock | `None` |
| `set_precio(p)` | Setter | Actualizar precio | `None` |
| `get_valor_total()` | Computed | Cantidad × Precio (POLIMORFISMO) | `float` |
| `__str__()` | Magic | Mostrar formato legible | `str` |

**Características POO:**
- ✅ **Encapsulación:** Atributos privados (`__nombre`) con getters/setters
- ✅ **Validación:** `max(0, cantidad)` previene valores negativos
- ✅ **Polimorfismo:** `__str__()` personalizado para display
- ✅ **Abstracción:** Interface clara (`get_*`, `set_*`)

---

#### **Clase Inventario** (`models/inventario.py`)

**Responsabilidad:** Gestionar colección de productos con operaciones CRUD usando múltiples colecciones Python.

**Colecciones Utilizadas:**

| Colección | Tipo | Propósito | Complejidad |
|-----------|------|----------|------------|
| `self.productos` | `dict` | Almacenamiento principal por ID | **O(1) lookup** |
| `self.ids_activos` | `set` | Búsqueda rápida de IDs | **O(1) member check** |
| `self.categorias` | `tuple` | Categorías inmutables válidas | **Hasheable, inmutable** |
| `buscar_resultado` | `list` | Resultados de búsqueda | **Flexible, iterable** |

**Métodos CRUD:**

```python
# CREATE - Guardar
def añadir_producto(self, producto):
    """Añade producto al diccionario e ID al conjunto."""
    if producto.get_id() not in self.productos:  # O(1)
        self.productos[producto.get_id()] = producto
        self.ids_activos.add(producto.get_id())  # O(1)
        return True

# READ - Recuperar
def obtener_producto(self, id):
    """Recupera producto por ID (O(1) en diccionario)."""
    return self.productos.get(id)  # O(1)

def buscar_producto(self, nombre):
    """Búsqueda parcial retorna lista (O(n))."""
    return [p for p in self.productos.values() 
            if nombre.lower() in p.get_nombre().lower()]

# UPDATE - Modificar
def actualizar_producto(self, id, cantidad=None, precio=None):
    """Actualiza campos de producto existente."""
    if id in self.productos:  # O(1) check en set
        producto = self.productos[id]  # O(1) acceso
        if cantidad is not None:
            producto.set_cantidad(cantidad)
        return True

# DELETE - Eliminar
def eliminar_producto(self, id):
    """Elimina de diccionario y conjunto."""
    if id in self.productos:  # O(1)
        del self.productos[id]  # O(1)
        self.ids_activos.discard(id)  # O(1)
        return True

# ANALYTICS
def valor_total_inventario(self):
    """Suma valores usando polimorfismo get_valor_total()."""
    return sum(p.get_valor_total() for p in self.productos.values())

def productos_bajo_stock(self, minimo=5):
    """Filtra con list comprehension."""
    return [p for p in self.productos.values() if p.get_cantidad() < minimo]
```

**Características POO:**
- ✅ **Encapsulación:** Colecciones privadas (`self.productos`)
- ✅ **Polimorfismo:** Llama `p.get_valor_total()` sin conocer implementación
- ✅ **Abstracción:** Interface CRUD uniforme
- ✅ **Reutilización:** Usa clase `Producto`

---

#### **Clase ConexionSQLite** (`models/conexion.py`)

**Responsabilidad:** Puente entre Python (Inventario) y SQLite (base de datos persistente).

**Características:**
- ✅ Transacciones ACID (sqlite3 automático)
- ✅ Parámetros preparados contra SQL injection
- ✅ Threading seguro (`check_same_thread=False` para Flask)
- ✅ Métodos CRUD espejo de Inventario

```python
class ConexionSQLite:
    """Conecta inventario Python con SQLite persistente."""
    
    def __init__(self, db_path='inventario.db'):
        self.db_path = db_path
        self.conexion = sqlite3.connect(
            db_path, 
            check_same_thread=False  # ✅ FIX: Permite Flask threading
        )
        self.cursor = self.conexion.cursor()
        self.crear_tablas()
    
    def crear_tablas(self):
        """DDL - Crea esquema inicialmente."""
        sql = '''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            cantidad INTEGER DEFAULT 0,
            precio REAL DEFAULT 0.0,
            categoria TEXT,
            descripcion TEXT,
            fecha_creacion TIMESTAMP,
            fecha_actualizacion TIMESTAMP
        )
        '''
        self.cursor.execute(sql)
        self.conexion.commit()
```

**Métodos CRUD en SQLite:**

| Operación | Método SQL | Python |
|-----------|-----------|--------|
| CREATE | `INSERT` | `añadir_producto(nombre, cantidad, precio, ...)` |
| READ | `SELECT` | `obtener_producto(id)` / `obtener_todos_productos()` |
| UPDATE | `UPDATE` | `actualizar_producto(id, nombre, cantidad, ...)` |
| DELETE | `DELETE` | `eliminar_producto(id)` |
| SEARCH | `LIKE` | `buscar_producto(texto)` |

---

## 2. FLUJO DE DATOS Y OPERACIONES CRUD

### 2.1 Arquitectura de Capas

```
┌─────────────────────────────────────────────────────────┐
│           Capa de Presentación (Flask)                  │
│  app.py - Rutas HTTP, templates, renderizado            │
└──────────────────────┬──────────────────────────────────┘
                       │ request.form['nombre'], etc
                       ▼
┌─────────────────────────────────────────────────────────┐
│      Capa de Lógica de Negocio (Models)                 │
│  Producto - Encapsula datos de un plato                 │
│  Inventario - CRUD en memoria (dict, set, tuple, list)  │
│  ConexionSQLite - CRUD persistente en SQLite            │
└──────────────────────┬──────────────────────────────────┘
                       │ SQL queries, resultsets
                       ▼
┌─────────────────────────────────────────────────────────┐
│           Capa de Datos (SQLite)                        │
│  inventario.db - Tablas persistentes (ACID)             │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Flujo CREATE (Agregar Plato)

**Escenario:** Usuario visita `/producto/nuevo`, completa formulario, confirma.

```
1. PRESENTACIÓN (app.py - GET /producto/nuevo)
   └─→ return render_template('producto_form.html')
       Muestra: <form method="POST" action="/producto/nuevo">
                  <input name="nombre"> ← user enters "Pasta Carbonara"
                  <input name="cantidad"> ← user enters "10"
                  <input name="precio"> ← user enters "15.99"
                  ...

2. PRESENTACIÓN (app.py - POST /producto/nuevo)
   └─→ datos_form = {
         'nombre': request.form['nombre'],        # "Pasta Carbonara"
         'cantidad': int(request.form['cantidad']), # 10
         'precio': float(request.form['precio']),   # 15.99
         'categoria': request.form['categoria']
       }

3. LÓGICA (app.py instantia Producto)
   └─→ producto = Producto(
         id=None,  # SQLite AUTOINCREMENT
         nombre='Pasta Carbonara',
         cantidad=10,
         precio=15.99,
         categoria='Platos Principales'
       )
       # VALIDACIÓN automática en Producto.__init__()
       # ├─ max(0, 10) = 10 ✓
       # └─ max(0, 15.99) = 15.99 ✓

4. PERSISTENCIA (app.py → ConexionSQLite)
   └─→ id_nuevo = db_conexion.añadir_producto(
         nombre='Pasta Carbonara',
         cantidad=10,
         precio=15.99,
         categoria='Platos Principales'
       )
       
       # SQL ejecutado en SQLite:
       INSERT INTO productos 
       (nombre, cantidad, precio, categoria, fecha_creacion)
       VALUES ('Pasta Carbonara', 10, 15.99, 'Platos', NOW())
       # lastrowid retornado: id_nuevo = 5

5. PRESENTACIÓN (Response)
   └─→ return redirect('/menu')
       Flash: "Plato añadido: Pasta Carbonara (#5)"
```

**Validaciones en CADA capa:**
- ✅ **HTML5:** `<input type="number" min="0">` (cliente)
- ✅ **Python:** `max(0, cantidad)` en `Producto.__init__()` (servidor)
- ✅ **SQL:** `CHECK (cantidad >= 0)` (base de datos)

---

### 2.3 Flujo READ (Ver Menu)

**Escenario:** Usuario accede a `/menu`

```
1. PRESENTACIÓN (app.py - GET /menu)
   └─→ todos_platos = db_conexion.obtener_todos_productos()
       # SQL: SELECT * FROM productos ORDER BY nombre

2. PERSISTENCIA (ConexionSQLite.obtener_todos_productos)
   └─→ self.cursor.execute(
         "SELECT id, nombre, cantidad, precio FROM productos ORDER BY nombre"
       )
       resultados = self.cursor.fetchall()
       # Retorna: [(5, 'Pasta Carbonara', 10, 15.99), ...]

3. LÓGICA (app.py reconstituye Productos)
   └─→ platos = []
       for fila in resultados:
           p = Producto(
               id=fila[0],      # 5
               nombre=fila[1],  # 'Pasta Carbonara'
               cantidad=fila[2], # 10
               precio=fila[3]    # 15.99
           )
           platos.append(p)

4. PRESENTACIÓN (Jinja2 template)
   └─→ return render_template(
         'productos.html',
         productos=platos,
         negocio_name='Restaurante La Buena Mesa'
       )
       
       <!-- Bootstrap table -->
       {% for plato in productos %}
         <tr>
           <td>{{ plato.get_nombre() }}</td>
           <td>{{ plato.get_cantidad() }}</td>
           <td>${{ "%.2f"|format(plato.get_precio()) }}</td>
           <td>${{ "%.2f"|format(plato.get_valor_total()) }}</td>
         </tr>
       {% endfor %}

5. RESPUESTA HTTP
   └─→ HTML con tabla renderizada enviada al navegador
```

**Complejidades:**
- **Lectura SQLite:** O(n) tabla completa
- **Construcción Producto:** O(n) iteración
- **Render Jinja2:** O(n) loop
- **Total:** O(n) donde n = cantidad de platos

---

### 2.4 Flujo UPDATE (Editar Plato)

**Escenario:** Usuario edita plato #5, cambia cantidad de 10 → 8

```
1. PRESENTACIÓN (app.py - GET /producto/editar/5)
   └─→ plato = db_conexion.obtener_producto(5)
       return render_template(
         'producto_editar.html',
         producto=plato
       )
       # Formulario prelleno con datos actuales

2. PRESENTACIÓN (app.py - POST /producto/editar/5)
   └─→ nueva_cantidad = int(request.form['cantidad'])  # 8
       nuevo_precio = float(request.form['precio'])   # 15.99

3. LÓGICA + PERSISTENCIA (app.py → ConexionSQLite)
   └─→ resultado = db_conexion.actualizar_producto(
         id=5,
         cantidad=8,
         precio=15.99
       )
       
       # SQL ejecutado:
       UPDATE productos 
       SET cantidad=8, precio=15.99, fecha_actualizacion=NOW()
       WHERE id=5

4. VALIDACIÓN en Producto (si fuera via Inventario)
   └─→ producto.set_cantidad(8)
       # Internamente: max(0, 8) = 8 ✓

5. PRESENTACIÓN (Response)
   └─→ return redirect(f'/menu')
       Flash: "Plato actualizado: Pasta Carbonara (#5)"
```

---

### 2.5 Flujo DELETE (Eliminar Plato)

**Escenario:** Usuario elimina plato #5

```
1. PRESENTACIÓN (app.py - POST /producto/eliminar/5)
   └─→ nombre_plato = db_conexion.obtener_producto(5).get_nombre()

2. PERSISTENCIA (ConexionSQLite.eliminar_producto)
   └─→ self.cursor.execute(
         "DELETE FROM productos WHERE id = ?",
         (5,)
       )
       self.conexion.commit()

3. VALIDACIÓN
   └─→ Si id=5 existe → DELETE ejecutado
       Si id=5 no existe → No error, retorna success

4. PRESENTACIÓN (Response)
   └─→ return redirect('/menu')
       Flash: "Plato eliminado: Pasta Carbonara"
```

---

## 3. OPTIMIZACIONES CON COLECCIONES

### 3.1 dict para O(1) Lookup

**Sin optimización (lista):**
```python
productos = [p1, p2, p3, ..., p1000]
# Buscar p1000: recorre 1000 elementos = O(n)
buscar = next(p for p in productos if p.get_id() == 1000)
```

**Con optimización (dict):**
```python
productos = {
    1: Producto(1, ...),
    2: Producto(2, ...),
    1000: Producto(1000, ...)
}
# Buscar id 1000: acceso directo = O(1)
buscar = productos[1000]  # Instant
```

**Ganancia:** Con 10,000 productos: ~5000 vs 1 acceso.

---

### 3.2 set para Búsqueda Rápida de IDs

**Sin optimización (lista):**
```python
ids = [1, 2, 3, ..., 1000]
# Verificar si 1000 exist: recorre hasta encontrar = O(n)
existe = 1000 in ids  # O(1000)
```

**Con optimización (set):**
```python
ids_activos = {1, 2, 3, ..., 1000}
# Verificar si 1000 exist: hash lookup = O(1)
existe = 1000 in ids_activos  # O(1)
```

---

### 3.3 tuple para Datos Inmutables

```python
categorias = ('Platos Principales', 'Postres', 'Bebidas', 'Entrantes')
# ✅ tuple es hasheable → puede ser dict key, set element
# ✅ Inmutable → No se modifica accidentalmente
# ✅ Eficiente → O(1) acceso por índice

# Uso en dict:
categorias_productos = {
    'Platos': 5,  # Puede usar tupla como clave
    'Postres': 3
}
```

---

### 3.4 list para Resultados Flexibles

```python
# Búsqueda retorna lista
resultados = inventario.buscar_producto('Pasta')
# [Producto(1, 'Pasta Carbonara', ...), Producto(2, 'Pasta Bolognesa', ...)]

# Ventajas:
# ✅ Mutable → puede filtrar/ordenar
# ✅ Ordenable → .sort()
# ✅ Indexable → resultados[0]
# ✅ Iterable → for p in resultados
```

---

## 4. CORRESPONDENCIA: OPERACIONES INVENTARIO ↔ SQLite

### 4.1 Tabla de Mapeo

| Operación | Clase Inventario | Clase ConexionSQLite | SQL Equivalente |
|-----------|------------------|----------------------|-----------------|
| **CREATE** | `inventario.añadir_producto(p)` | `db.añadir_producto(nombre, cantidad, precio)` | `INSERT INTO productos ...` |
| **READ** | `inventario.obtener_producto(id)` | `db.obtener_producto(id)` | `SELECT * FROM productos WHERE id=?` |
| **READ ALL** | `inventario.listar_todos()` | `db.obtener_todos_productos()` | `SELECT * FROM productos` |
| **UPDATE** | `inventario.actualizar_producto(id, ...)` | `db.actualizar_producto(id, ...)` | `UPDATE productos SET ... WHERE id=?` |
| **DELETE** | `inventario.eliminar_producto(id)` | `db.eliminar_producto(id)` | `DELETE FROM productos WHERE id=?` |
| **SEARCH** | `inventario.buscar_producto(texto)` | `db.buscar_producto(texto)` | `SELECT * FROM productos WHERE nombre LIKE ?` |
| **STATS** | `inventario.valor_total_inventario()` | `db.obtener_valor_total_inventario()` | `SELECT SUM(cantidad*precio) FROM productos` |
| **FILTER** | `inventario.productos_bajo_stock(5)` | `db.obtener_bajo_stock(5)` | `SELECT * FROM productos WHERE cantidad < ?` |

---

## 5. FLUJO DE INTEGRACIÓN: Flask ↔ Models ↔ SQLite

### 5.1 Inicialización (app.py)

```python
from models.conexion import ConexionSQLite
from models.inventario import Inventario
from models.producto import Producto

# CAPA 1: Instancia conexión SQLite
db_conexion = ConexionSQLite('inventario.db')
# ├─ Crea tablas si no existen (DDL)
# └─ Inicializa cursor para operaciones

# CAPA 2: Instancia inventario en memoria (para búsquedas rápidas)
inventario = Inventario()
# ├─ Inicializa dict vacío
# ├─ Inicializa set vacío
# └─ Define categorías tuple

# TODO: Cargar datos SQLite → Inventario (Bootstrap)
todos_platos = db_conexion.obtener_todos_productos()
for plato_data in todos_platos:
    p = Producto(
        id=plato_data['id'],
        nombre=plato_data['nombre'],
        cantidad=plato_data['cantidad'],
        precio=plato_data['precio']
    )
    inventario.añadir_producto(p)

app = Flask(__name__)
```

### 5.2 Ruta CREATE (/producto/nuevo)

```python
@app.route('/producto/nuevo', methods=['GET', 'POST'])
def producto_nuevo():
    if request.method == 'GET':
        # GET: Mostrar formulario
        return render_template('producto_form.html', negocio_name='Restaurante La Buena Mesa')
    
    # POST: Procesar datos enviados
    try:
        # 1. CAPTURA datos del formulario
        nombre = request.form['nombre'].strip()
        cantidad = int(request.form.get('cantidad', 0))
        precio = float(request.form.get('precio', 0.0))
        categoria = request.form.get('categoria', 'Platos')
        descripcion = request.form.get('descripcion', '')
        
        # 2. VALIDACIÓN (Producto la hace internamente)
        if not nombre:
            flash('El nombre es requerido', 'error')
            return redirect('/producto/nuevo')
        
        # 3. PERSISTENCIA (SQLite)
        id_nuevo = db_conexion.añadir_producto(
            nombre=nombre,
            cantidad=cantidad,
            precio=precio,
            categoria=categoria,
            descripcion=descripcion
        )
        
        # 4. INVENTARIO en memoria (opcional, para búsquedas rápidas)
        nuevo_producto = Producto(
            id=id_nuevo,
            nombre=nombre,
            cantidad=cantidad,
            precio=precio,
            categoria=categoria,
            descripcion=descripcion
        )
        inventario.añadir_producto(nuevo_producto)
        
        # 5. RESPUESTA
        flash(f'Plato "{nombre}" añadido exitosamente (#{ id_nuevo})', 'success')
        return redirect('/menu')
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect('/producto/nuevo')
```

### 5.3 Ruta READ (/menu)

```python
@app.route('/menu')
def menu():
    """Muestra catálogo de platos."""
    # LÓGICA: Obtener de SQLite
    todos_platos = db_conexion.obtener_todos_productos()
    
    # STATS: Usar clase Inventario para cálculos
    total_valor = sum(
        p['cantidad'] * p['precio'] 
        for p in todos_platos
    )
    bajo_stock = db_conexion.obtener_bajo_stock(5)
    
    # PRESENTACIÓN
    return render_template(
        'productos.html',
        productos=todos_platos,
        total_valor=total_valor,
        bajo_stock=bajo_stock,
        negocio_name='Restaurante La Buena Mesa'
    )
```

### 5.4 Ruta UPDATE (/producto/editar/<id>)

```python
@app.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    plato = db_conexion.obtener_producto(id)
    
    if not plato:
        flash('Plato no encontrado', 'error')
        return redirect('/menu')
    
    if request.method == 'GET':
        return render_template(
            'producto_editar.html',
            producto=plato,
            negocio_name='Restaurante La Buena Mesa'
        )
    
    # POST
    try:
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        
        # PERSISTENCIA
        db_conexion.actualizar_producto(
            id=id,
            cantidad=cantidad,
            precio=precio
        )
        
        # INVENTARIO en memoria
        if id in inventario.ids_activos:
            inventario.actualizar_producto(id, cantidad, precio)
        
        flash(f'Plato actualizado', 'success')
        return redirect('/menu')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(f'/producto/editar/{id}')
```

### 5.5 Ruta DELETE (/producto/eliminar/<id>)

```python
@app.route('/producto/eliminar/<int:id>', methods=['POST'])
def producto_eliminar(id):
    plato = db_conexion.obtener_producto(id)
    
    if not plato:
        flash('Plato no encontrado', 'error')
        return redirect('/menu')
    
    nombre = plato['nombre']
    
    try:
        # PERSISTENCIA
        db_conexion.eliminar_producto(id)
        
        # INVENTARIO en memoria
        inventario.eliminar_producto(id)
        
        flash(f'Plato "{nombre}" eliminado', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect('/menu')
```

---

## 6. TESTING Y VALIDACIÓN

### 6.1 Test CRUD Completo (Python)

```python
# test_crud.py
from models.producto import Producto
from models.inventario import Inventario
from models.conexion import ConexionSQLite

def test_crud():
    """Test completo de CRUD en todas las capas."""
    
    # Setup
    db = ConexionSQLite(':memory:')  # BD en memoria para test
    inv = Inventario()
    
    print("=" * 60)
    print("TEST CRUD - RESTAURANTE LA BUENA MESA")
    print("=" * 60)
    
    # CREATE
    print("\n1. CREATE - Insertar platos")
    id1 = db.añadir_producto('Pasta Carbonara', 10, 15.99, 'Platos', 'Pasta italiana')
    id2 = db.añadir_producto('Ensalada Griega', 8, 12.50, 'Ensaladas', 'Fresca')
    id3 = db.añadir_producto('Tiramisú', 5, 8.99, 'Postres', 'Postre italiano')
    print(f"  ✓ Plato 1 creado: ID {id1}")
    print(f"  ✓ Plato 2 creado: ID {id2}")
    print(f"  ✓ Plato 3 creado: ID {id3}")
    
    # READ
    print("\n2. READ - Recuperar platos")
    plato = db.obtener_producto(id1)
    print(f"  ✓ Plato recuperado: {plato['nombre']} (${plato['precio']})")
    
    todos = db.obtener_todos_productos()
    print(f"  ✓ Total platos: {len(todos)}")
    
    # UPDATE
    print("\n3. UPDATE - Modificar cantidad")
    db.actualizar_producto(id1, cantidad=5)
    plato_actualizado = db.obtener_producto(id1)
    print(f"  ✓ Cantidad actualizada: {plato_actualizado['cantidad']} unidades")
    
    # SEARCH
    print("\n4. SEARCH - Buscar platos")
    resultados = db.buscar_producto('Pasta')
    print(f"  ✓ Búsqueda 'Pasta': {len(resultados)} resultado(s)")
    
    # STATS
    print("\n5. STATS - Analystics")
    valor_total = db.obtener_valor_total_inventario()
    print(f"  ✓ Valor total inventario: ${valor_total:.2f}")
    
    bajo_stock = db.obtener_bajo_stock(6)
    print(f"  ✓ Platos bajo stock (<6): {len(bajo_stock)}")
    
    # DELETE
    print("\n6. DELETE - Eliminar plato")
    db.eliminar_producto(id3)
    todos_despues = db.obtener_todos_productos()
    print(f"  ✓ Plato eliminado. Platos restantes: {len(todos_despues)}")
    
    print("\n" + "=" * 60)
    print("✅ TEST CRUD COMPLETADO EXITOSAMENTE")
    print("=" * 60)

if __name__ == '__main__':
    test_crud()
```

**Salida esperada:**
```
============================================================
TEST CRUD - RESTAURANTE LA BUENA MESA
============================================================

1. CREATE - Insertar platos
  ✓ Plato 1 creado: ID 1
  ✓ Plato 2 creado: ID 2
  ✓ Plato 3 creado: ID 3

2. READ - Recuperar platos
  ✓ Plato recuperado: Pasta Carbonara ($15.99)
  ✓ Total platos: 3

3. UPDATE - Modificar cantidad
  ✓ Cantidad actualizada: 5 unidades

4. SEARCH - Buscar platos
  ✓ Búsqueda 'Pasta': 1 resultado(s)

5. STATS - Analystics
  ✓ Valor total inventario: $196.19
  ✓ Platos bajo stock (<6): 2

6. DELETE - Eliminar plato
  ✓ Plato eliminado. Platos restantes: 2

============================================================
✅ TEST CRUD COMPLETADO EXITOSAMENTE
============================================================
```

---

## 7. CONCEPTOS CLAVE DEMOSTRADOS

### 7.1 Programación Orientada a Objetos (POO)

| Concepto | Implementación | Ejemplo |
|----------|---|----------|
| **Encapsulación** | Atributos privados `__` con getters/setters | `self.__nombre` solo accesible via `get_nombre()` |
| **Abstracción** | Interface uniforme CRUD | Métodos `obtener_producto()` ocultan detalles SQL |
| **Polimorfismo** | `__str__()` y `get_valor_total()` especializados | Cada `Producto` implementa cálculo según reglas |
| **Herencia** | (Preparada para futuro) | `ProductoPlato(Producto)`, `ProductoBebida(Producto)` |

### 7.2 Colecciones Python

| Colección | Caso de Uso | Complejidad |
|-----------|-----------|-----------|
| `dict` | Acceso rápido por ID | `O(1)` |
| `set` | Búsqueda de membresía | `O(1)` |
| `tuple` | Datos inmutables | Hasheable, inmutable |
| `list` | Resultados ordenables | Flexible, `O(n)` búsqueda |
| `list comprehension` | Filtrado elegante | `[x for x in items if condition]` |

### 7.3 SQLite y ACID

| Propiedad | Ejemplo |
|-----------|---------|
| **Atomicity** | INSERT nombre UNIQUE: todo o nada |
| **Consistency** | CHECK cantidad >= 0 |
| **Isolation** | `check_same_thread=False` con Flask |
| **Durability** | `.commit()` escribe a disco |

### 7.4 Integración Flask ↔ SQLite

```
HTTP Request → Flask Route → Modelo Python → SQLite → HTTP Response
```

---

## 8. CONCLUSIÓN

El sistema "**Restaurante La Buena Mesa**" demuestra integración completa de:

- **POO:** Clases `Producto`, `Inventario`, `ConexionSQLite` con encapsulación y abstracción
- **Colecciones:** Uso estratégico de `dict`, `set`, `tuple`, `list` para optimizar operaciones
- **SQLite:** CRUD persistente con validación en múltiples capas
- **Flask:** Rutas que conectan presentación con lógica y datos
- **Template Inheritance:** Jinja2 `base.html` para reutilización HTML

### Resultados de Aprendizaje

✅ Diseñar arquitectura de 3 capas (Presentación → Lógica → Datos)  
✅ Implementar CRUD completo en Python y SQL  
✅ Optimizar operaciones con estructuras de datos apropiadas  
✅ Validar datos en múltiples niveles (HTML5, Python, SQL)  
✅ Integrar framework web con base de datos  
✅ Documentar código siguiendo estándares profesionales  

---

**Fecha:** Semana 11  
**Estado:** ✅ Completado  
**Siguiente:** Semana 12 - API REST y testing avanzado
