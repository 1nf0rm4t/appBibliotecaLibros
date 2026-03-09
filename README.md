# Biblioteca App

Aplicación web desarrollada en Python con Flask para la gestión de una biblioteca, incluyendo Autores, Editoriales y Libros.

## Características

*   **Gestión de Autores**: Crear, editar, listar y eliminar autores con su respectiva información biográfica.
*   **Gestión de Editoriales**: Administrar un catálogo de editoriales especificando el país de procedencia.
*   **Gestión de Libros**: Registro de libros vinculando su Autor y su Editorial, así como datos de publicación (ISBN, Año).
*   **Listados Avanzados**: Todas las vistas de listado soportan **búsqueda de texto completo**, **ordenación avanzada** bidireccional por cada columna y **paginación** integrada.
*   **Interfaz de Usuario**: Interfaz responsiva y estilizada con CSS plano, y el uso del motor de plantillas Jinja2.

## Requisitos Técnicos

*   Python 3.x
*   Flask 3.0.0
*   Flask-SQLAlchemy 3.1.1
*   Base de datos MariaDB (Pymysql 1.1.0)
*   Cryptography 42.0.5

## Configuración y Despliegue

1. **Clonar repositorio** e ir al directorio de la aplicación.
2. **Instalar dependencias**: `pip install -r requirements.txt`
3. **Configurar Base de Datos**: Asegurarse de tener MariaDB en ejecución y una base de datos creada llamada `biblioteca` o la especificada en la variable de entorno `DATABASE_URL`.
   * Cadena de conexión por defecto modificable en `app.py`: `mysql+pymysql://root:1234@localhost/biblioteca`
4. **Ejecutar aplicación**: `python3 app.py` (esto creará las tablas automáticamente gracias a `db.create_all()`).

La aplicación estará disponible en `http://127.0.0.1:5000`.
