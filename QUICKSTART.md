# Guía Rápida de Inicio - Semana 12

## Instalación Rápida

### 1. Windows - PowerShell

```powershell
# Crear y activar entorno virtual
python -m venv .venv
.\.venv\Scripts\Activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
python test_semana12.py

# Iniciar aplicación
python app.py
```

### 2. Linux / Mac

```bash
# Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
python3 test_semana12.py

# Iniciar aplicación
python3 app.py
```

## Primeros Pasos

### Acceso a la Aplicación

Una vez que ejecute `python app.py`, la aplicación estará disponible en:

```
http://localhost:5000/
```

### Rutas Principales

| Ruta | Descripción |
|------|-------------|
| `/` | Página principal |
| `/productos` | Listado de productos |
| `/producto/nuevo` | Crear nuevo producto |
| `/datos` | **Ver datos de todas las fuentes** |
| `/reportes` | Reportes del inventario |
| `/buscar` | Buscar productos |

## Uso de Utilidades

### Desde el Script

```bash
# Menú interactivo
python utilidades.py

# Comandos directos
python utilidades.py backup          # Crear respaldo
python utilidades.py restore         # Restaurar respaldo
python utilidades.py sync            # Sincronizar archivos
python utilidades.py info            # Ver información
python utilidades.py export json     # Exportar a JSON
```

## Estructura de Directorios Importante

```
inventario_sistema/
├── .venv/               # Entorno virtual
├── inventario/          # Paquete principal
│   ├── __init__.py
│   ├── bd.py           # Configuración SQLAlchemy
│   ├── productos.py    # Modelo Producto
│   ├── inventario.py   # Gestor de inventario
│   ├── persistencia.py # Funciones de persistencia
│   └── data/           # Archivos de datos
│       ├── datos.txt
│       ├── datos.json
│       └── datos.csv
├── models/             # Modelos alternativos
├── static/             # CSS, JS,imágenes
├── templates/          # Plantillas HTML
├── app.py             # Aplicación principal
├── test_semana12.py   # Tests
└── utilidades.py      # Herramientas
```

## Operaciones Comunes

### Crear un Producto

Desde Python:

```python
from app import app, db
from inventario import GestorInventario

with app.app_context():
    producto = GestorInventario.crear_producto(
        nombre="Ceviche",
        precio=12.50,
        cantidad=8,
        categoria="Mariscos"
    )
    print(f"Creado: {producto.nombre}")
```

Desde la Web:
1. Ir a `/producto/nuevo`
2. Completar el formulario
3. Enviar

### Ver Todos los Datos

Visita: http://localhost:5000/datos

Allí verás los datos de todas las fuentes de persistencia:
- SQLite
- JSON
- CSV
- TXT

### Ejecutar Tests

```bash
python test_semana12.py
```

Esto ejecutará 13 tests para validar:
- ✅ Crear productos
- ✅ Obtener productos
- ✅ Actualizar productos
- ✅ Eliminar productos
- ✅ Validación de datos
- ✅ Persistencia en TXT, JSON, CSV
- ✅ Sincronización de múltiples fuentes

## Solución de Problemas

### Error: ModuleNotFoundError: No module named 'flask'

**Solución:**
```bash
pip install -r requirements.txt
```

### Error: database is locked

**Solución:** Cierra la aplicación Flask y borre `inventario.db`
```bash
rm inventario.db  # Linux/Mac
del inventario.db  # Windows
```

### Error: Archivo datos.json corrupto

**Solución:** Use las utilidades para sincronizar:
```bash
python utilidades.py sync
```

### La aplicación no inicia

**Comprobaciones:**
1. ¿Entorno virtual activado? (`which python` o `which python3`)
2. ¿Dependencias instaladas? (`pip list`)
3. ¿Puerto 5000 disponible?

## Documentación Disponible

| Archivo | Contenido |
|---------|-----------|
| `README_SEMANA12.md` | Documentación completa de la implementación |
| `API_REFERENCE.md` | Referencia completa de la API |
| `ejemplos_uso.py` | Ejemplos de código |
| `test_semana12.py` | Tests automatizados |

## Flujo de Trabajo Típico

1. **Iniciar aplicación**: `python app.py`
2. **Acceder a web**: Abrir navegador en `http://localhost:5000`
3. **Crear datos**: Click en "Agregar Producto"
4. **Visualizar datos**: Ir a `/datos`
5. **Exportar datos**: Usar utilidades para backup
6. **Cerrar**: Ctrl+C en terminal

## Sincronización Automática

Cuando creas o actualizas un producto, automáticamente se guarda en:
- ✅ Base de datos SQLite
- ✅ Archivo JSON
- ✅ Archivo CSV
- ✅ Archivo TXT

No necesitas hacer nada manualmente.

## Backups

Se crean automáticamente en la carpeta `backups/`:

```
backups/
├── backup_20260302_103045/
│   ├── inventario.db
│   ├── datos.txt
│   ├── datos.json
│   └── datos.csv
├── backup_20260302_120000/
│   └── ...
```

### Crear Backup Manual

```bash
python utilidades.py backup
```

### Restaurar Backup

```bash
python utilidades.py restore
```

## Próximos Pasos

1. ✅ Familiarízate con la aplicación web
2. ✅ Crea varios productos de prueba
3. ✅ Visita `/datos` para ver la sincronización
4. ✅ Lee `API_REFERENCE.md` para entender la API
5. ✅ Ejecuta `test_semana12.py` para validar
6. ✅ Personaliza los modelos según tus necesidades

## Contacto y Soporte

Para preguntas o problemas, consulta:
- `README_SEMANA12.md` - Documentación técnica
- `API_REFERENCE.md` - Referencia de funciones
- `ejemplos_uso.py` - Ejemplos de código

---

**¡Listo! Ya estás preparado para trabajar con Semana 12.**
