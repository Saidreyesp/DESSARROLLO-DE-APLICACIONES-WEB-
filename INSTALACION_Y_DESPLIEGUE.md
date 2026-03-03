# Guía de Instalación y Despliegue del Sistema de Gestión de Inventario

## 1. Instalación Local

### Prerequisitos
- Python 3.11+
- Git
- Visual Studio Code o PyCharm

### Pasos de Instalación

#### 1.1 Clonar o descargar el proyecto
```bash
git clone https://github.com/tuusuario/inventario_sistema.git
cd inventario_sistema
```

#### 1.2 Crear entorno virtual
```bash
# En Windows
python -m venv venv
.\venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 1.3 Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 1.4 Ejecutar la aplicación
```bash
python app.py
```

Acceder a: `http://localhost:5000`

---

## 2. Estructura del Proyecto

```
inventario_sistema/
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias
├── Procfile                    # Configuración para Render
├── runtime.txt                 # Versión de Python
├── .gitignore                  # Archivos ignorados por Git
├── .env.example                # Variables de entorno (ejemplo)
├── README.md                   # Este archivo
│
├── models/
│   ├── producto.py             # Clase Producto (POO)
│   ├── inventario.py           # Clase Inventario (Colecciones)
│   └── conexion.py             # Clase ConexionSQLite
│
├── inventario/
│   ├── bd.py                   # SQLAlchemy ORM
│   ├── productos.py            # Modelo ORM
│   └── persistencia.py         # Persistencia de datos
│
├── templates/
│   ├── index.html              # Dashboard
│   ├── productos.html          # Listado de productos
│   ├── producto_form.html      # Crear producto
│   ├── producto_editar.html    # Editar producto
│   ├── producto_detalle.html   # Detalle del producto
│   ├── buscar.html             # Búsqueda
│   ├── bajo_stock.html         # Productos bajo stock
│   ├── reportes.html           # Reportes
│   ├── error_404.html          # Error 404
│   └── error_500.html          # Error 500
│
├── static/
│   └── style.css               # Estilos CSS
│
└── inventario.db               # Base de datos (generada automáticamente)
```

---

## 3. Despliegue en Render

### 3.1 Crear cuenta en Render
1. Ir a https://render.com
2. Registrarse con GitHub

### 3.2 Conectar repositorio GitHub
1. Hacer push del proyecto a GitHub
2. En Render: New+ > Web Service
3. Seleccionar el repositorio

### 3.3 Configurar el servicio
- **Name**: inventario-sistema (o el nombre que prefieras)
- **Runtime**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Environment Variables**:
  - `FLASK_ENV=production`
  - `SECRET_KEY=tu_clave_secreta_aqui`

### 3.4 Deploy
Render desplegará automáticamente. La URL será algo como:
`https://inventario-sistema.onrender.com`

---

## 4. Variables de Entorno

Crear archivo `.env` local (NO incluir en Git):
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui_cambiar_en_produccion
DATABASE_URL=sqlite:///inventario.db
```

---

## 5. Comandos Útiles

```bash
# Activar entorno virtual
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python app.py

# Desactivar entorno virtual
deactivate

# Ver requisitos instalados
pip list

# Generar requirements.txt
pip freeze > requirements.txt
```

---

## 6. Características Implementadas

### Semana 11 (POO + Colecciones + SQLite)
✅ Clase Producto con POO
✅ Clase Inventario con colecciones (dict, list, set, tuple)
✅ Clase ConexionSQLite con CRUD completo
✅ 10+ plantillas HTML
✅ Rutas dinámicas y CRUD
✅ Dashboard con estadísticas
✅ Búsqueda y filtrado
✅ Alertas de bajo stock

### Semana 12 (Persistencia + GitHub + Render)
✅ Persistencia en archivos (TXT/JSON/CSV)
✅ SQLAlchemy ORM
✅ Control de versiones con Git/GitHub
✅ Despliegue en Render
✅ Procfile y runtime.txt
✅ Variables de entorno
✅ .gitignore
✅ Documentación completa

---

## 7. Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solución**: Asegúrate de activar el entorno virtual e instalar dependencias
```bash
pip install -r requirements.txt
```

### Error: "Database is locked"
**Solución**: Cierra todas las instancias de la aplicación y borra `inventario.db`

### Error en Render: "SyntaxError"
**Solución**: Verifica que Python 3.11 esté en `runtime.txt`

### Error de conexión a BD
**Solución**: Borra `inventario.db` y reinicia la aplicación

---

## 8. Tips para GitHub

### Crear repositorio local
```bash
git init
git add .
git commit -m "Inicial: Sistema de Gestion de Inventario"
git branch -M main
git remote add origin <URL_DEL_REPO>
git push -u origin main
```

### Hacer cambios y push
```bash
git add .
git commit -m "Descripción de cambios"
git push
```

---

## 9. Contacto y Soporte

Para preguntas o problemas:
- Revisa la documentación del código
- Consul ta la documentación de Flask: https://flask.palletsprojects.com/
- Documentación de SQLAlchemy: https://www.sqlalchemy.org/

---

**Última actualización**: Marzo 2026
**Versión**: 1.0
**Estado**: Producción Ready
