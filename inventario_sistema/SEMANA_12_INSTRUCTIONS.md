# SEMANA 12: Persistencia de Datos Avanzada

## Introducción

En esta semana continuaremos desarrollando el proyecto Flask iniciado en la Semana 9, estructurado con plantillas en la Semana 10 y con CRUD + SQLite en la Semana 11 y la persistencia en la Semana 12.

Ahora el objetivo es ampliar el sistema incorporando diferentes mecanismos de persistencia de datos:

- **Archivos JSON, TXT, CSV**
- **Base de datos SQLite utilizando SQLAlchemy (ORM)**

### Notas Importantes

- **Esta semana NO se crea un nuevo proyecto.**
- **Se debe continuar trabajando en la misma carpeta del proyecto desarrollado en semanas anteriores.**

## Descripción de la Tarea

El objetivo de esta tarea es que los estudiantes amplíen su proyecto Flask creado en las semanas anteriores (o lo configuren si aún no lo han hecho), incorporando persistencia de datos utilizando archivos locales (TXT, JSON, CSV) y una base de datos SQLite. Además, deberán subir el código actualizado a su repositorio de GitHub.

## Instrucciones Detalladas

### 1. Si aún no tienes el proyecto Flask creado

Sigue las instrucciones de tareas anteriores para:
- Configurar un entorno virtual en PyCharm o Visual Studio Code e instalar Flask.
- Crear la estructura del proyecto Flask con el archivo `app.py`.
- Definir rutas básicas y verificar que la aplicación funcione.

**Si ya tienes el proyecto, continúa con los siguientes pasos.**

### 2. Agregar Persistencia de Datos a la Aplicación Flask

#### 2.1. Verifica que tu proyecto tenga la siguiente estructura

```
Proyecto/
├── app.py
├── form.py
├── requirements.txt
├── .gitignore
├── __init__.py
│
├── inventario/
│   ├── __init__.py
│   ├── bd.py
│   ├── inventario.py
│   ├── productos.py
│   └── data/
│       ├── datos.txt
│       ├── datos.json
│       └── datos.csv
│
├── static/
│   └── (tu css aquí, por ejemplo: css/style.css)
│
└── templates/
    ├── base.html
    ├── index.html
    ├── contactos.html
    ├── productos.html
    ├── producto_form.html
    └── datos.html   (NUEVO para Semana 12)
```

#### 2.2. Persistencia con Archivos TXT, JSON y CSV

La aplicación debe permitir recibir datos desde un formulario y almacenarlos en archivos dentro del proyecto. Asimismo, deberá existir al menos una ruta que permita leer la información almacenada en cada formato y mostrarla en una plantilla HTML.

**Requisitos:**

1. **Para la persistencia en formato TXT:** utilizar la función `open()` en modo escritura y lectura.

2. **Para el formato JSON:** utilizar la librería `json`, convirtiendo previamente los datos a diccionario antes de almacenarlos, y empleando los métodos correspondientes para guardar y leer información.

3. **Para el formato CSV:** utilizar la librería `csv`, implementando la escritura y lectura de registros mediante los métodos adecuados.

#### 2.3. Persistencia con SQLite utilizando SQLAlchemy

Implementar los siguientes pasos:

1. **Instalar SQLAlchemy**
2. **Modificar `app.py`** para conectar con SQLite
3. **Definir rutas** para interactuar con la base de datos
4. **Guardar datos** en la base de datos SQLite
5. **Leer datos** almacenados en la base de datos SQLite

#### 2.4. Definir el modelo de datos

Crear un modelo (por ejemplo `Producto`, `Usuario` u otro según el proyecto) que contenga:

- `id` (clave primaria)
- `nombre`
- Atributos adicionales según el sistema (precio, cantidad, email, etc.)

## Información de Referencia

Para esta semana, deberás:

1. ✅ Crear/Actualizar modelos con SQLAlchemy
2. ✅ Implementar funciones de persistencia en TXT, JSON y CSV
3. ✅ Implementar CRUD con SQLite
4. ✅ Crear rutas para mostrar y gestionar datos desde múltiples fuentes
5. ✅ Actualizar plantillas HTML para visualizar datos
6. ✅ Subir cambios a GitHub

## Archivos a Revisar/Crear

- `inventario/bd.py` - Configuración de base de datos
- `inventario/productos.py` - Modelos
- `inventario/inventario.py` - Lógica de persistencia (TXT, JSON, CSV)
- `inventario/data/` - Carpeta para almacenar archivos de datos
- `templates/datos.html` - Nueva plantilla para visualizar datos

## Notas Importantes

- Todas las funciones de persistencia deben ser reutilizables y documentadas
- Manejar excepciones adecuadamente en operaciones de archivo y base de datos
- Validar datos antes de almacenarlos
- Asegurar que el código sea escalable y mantenible
- Subir cambios regularmente a GitHub

---

**Última actualización:** Marzo 2026  
**Semana:** 12
