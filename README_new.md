# Restaurante La Buena Mesa - Sistema de Gestión Flask

Un sistema completo de gestión de restaurante desarrollado en **Flask** con **Jinja2**, **SQLAlchemy**, y **SQLite**.

## Características

- ✅ **Gestión de Menú**: Añadir, editar, eliminar y buscar platos
- ✅ **Sistema de Reservas**: Reserva de mesas con clientes
- ✅ **Plantillas Dinámicas**: Herencia de templates con Jinja2
- ✅ **Base de Datos SQLite**: Persistencia de datos con SQLAlchemy
- ✅ **Interfaz Bootstrap**: Diseño responsivo y moderno
- ✅ **Rutas Dinámicas**: Acceso a platos y clientes individualmente
- ✅ **Reportes**: Análisis de inventario y bajo stock

## Estructura del Proyecto

```
restaurante-sistema/
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias del proyecto
├── .gitignore                  # Archivos ignorados por Git
├── .env.example                # Variables de entorno ejemplo
├── inventario.db              # Base de datos SQLite
│
├── templates/
│   ├── base.html              # Template base (herencia)
│   ├── index.html             # Página de inicio
│   ├── about.html             # Acerca de
│   ├── productos.html         # Menú completo
│   ├── plato.html             # Detalle de plato individual
│   ├── reserva.html           # Confirmación de reserva
│   ├── producto_form.html     # Formulario nuevo plato
│   ├── producto_editar.html   # Formulario editar plato
│   ├── buscar.html            # Búsqueda de platos
│   ├── bajo_stock.html        # Platos con bajo stock
│   ├── reportes.html          # Reportes y estadísticas
│   ├── datos.html             # Vista de datos persistidos
│   ├── error_404.html         # Página no encontrada
│   └── error_500.html         # Error del servidor
│
├── static/
│   └── style.css              # Estilos CSS personalizados
│
├── models/
│   ├── __init__.py
│   ├── producto.py            # Clase Producto (POO)
│   ├── inventario.py          # Clase Inventario (colecciones)
│   └── conexion.py            # Helper SQLite
│
├── inventario/
│   ├── __init__.py
│   ├── bd.py                  # Instancia SQLAlchemy
│   ├── productos.py           # Modelo ORM Producto
│   └── persistencia.py        # Funciones TXT/JSON/CSV
│
└── README.md                  # Este archivo
```

## Requisitos

- Python 3.8+
- pip (gestor de paquetes)

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/restaurante-sistema.git
cd restaurante-sistema
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación localmente
```bash
python app.py
```

La aplicación estará disponible en: **http://127.0.0.1:5000**

### Rutas principales

| Ruta | Descripción |
|------|-------------|
| `/` | Página de inicio / Dashboard |
| `/menu` | Menú completo de platos |
| `/plato/<nombre>` | Detalle de un plato (ruta dinámica) |
| `/reserva/<cliente>` | Reserva para un cliente (ruta dinámica) |
| `/producto/nuevo` | Formulario para añadir plato |
| `/producto/editar/<id>` | Formulario para editar plato |
| `/buscar` | Búsqueda de platos |
| `/bajo-stock` | Platos con stock bajo |
| `/reportes` | Reportes y estadísticas |
| `/about` | Información sobre el restaurante |

## Ejemplos de Rutas Dinámicas

```bash
# Ver un plato específico
http://127.0.0.1:5000/plato/Ensalada%20Cesar

# Hacer una reserva (cliente específico)
http://127.0.0.1:5000/reserva/Juan

# Hacer una reserva (otro cliente)
http://127.0.0.1:5000/reserva/Maria
```

## Tecnologías Utilizadas

- **Backend**: Flask 3.1.2
- **ORM**: Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.48
- **Base de Datos**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.0
- **Plantillas**: Jinja2
- **Control de Versiones**: Git/GitHub

## Persistencia de Datos

La aplicación soporta múltiples formatos de persistencia:

- **SQLite**: Base de datos relacional (`inventario.db`)
- **JSON**: Formato `datos.json`
- **CSV**: Formato tabulado `datos.csv`
- **TXT**: Líneas de JSON `datos.txt`

## Despliegue en Render

### Desde GitHub:

1. Sube tu proyecto a GitHub
2. Ve a [Render.com](https://render.com)
3. Crea un nuevo "Web Service"
4. Conecta tu repositorio de GitHub
5. Configura:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Despliega

**Variables de entorno** (en Render):
```
FLASK_ENV=production
FLASK_DEBUG=False
```

## Contribución

Si deseas contribuir:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Agregar mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## Autor

Desarrollado como proyecto educativo para el curso de **Desarrollo Web con Flask**.

---

**Versión**: 2.0 (Semana 10 - Plantillas con Herencia)  
**Última actualización**: Marzo 2026
