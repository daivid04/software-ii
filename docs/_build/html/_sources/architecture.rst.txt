Introducción a la Arquitectura
==============================

Visión General
--------------

El sistema de **Taller Diego** está organizado en capas que separan responsabilidades:

.. code-block:: text

    ┌─────────────────────────────────────┐
    │      Frontend (HTML/JavaScript)     │
    └──────────────┬──────────────────────┘
                   │ REST API
                   ▼
    ┌─────────────────────────────────────┐
    │        Routes (FastAPI)             │
    │  - POST /productos                  │
    │  - GET /ordenes/{id}                │
    │  - DELETE /ventas/{id}              │
    └──────────────┬──────────────────────┘
                   │
    ┌──────────────▼──────────────────────┐
    │      Services (Business Logic)      │
    │  - Validaciones                     │
    │  - Transacciones                    │
    │  - Control de stock                 │
    └──────────────┬──────────────────────┘
                   │
    ┌──────────────▼──────────────────────┐
    │   Repositories (Data Access)        │
    │  - CRUD Operations                  │
    │  - Queries complejas                │
    │  - Row-level locking                │
    └──────────────┬──────────────────────┘
                   │
    ┌──────────────▼──────────────────────┐
    │    Models (SQLAlchemy/PostgreSQL)   │
    │  - Producto                         │
    │  - Autoparte                        │
    │  - Orden                            │
    └─────────────────────────────────────┘

Conceptos Clave
---------------

Modelos (Models)
~~~~~~~~~~~~~~~~

Los modelos representan las entidades de la base de datos:

- **Producto**: Artículo base con atributos comunes
- **Autoparte**: Herencia de Producto con modelo y año
- **Servicio**: Servicio prestado
- **Empleado**: Trabajador del taller
- **Orden**: Orden de servicio con servicios y empleados
- **Venta**: Venta de productos con líneas de detalle

Relaciones:

- `OrdenServicio`: Junction table (Orden ↔ Servicio)
- `OrdenEmpleado`: Many-to-many (Orden ↔ Empleado)
- `VentaProducto`: Junction table con control de stock (Venta ↔ Producto)

Esquemas (Schemas)
~~~~~~~~~~~~~~~~~~

Schemas Pydantic para validación de entrada/salida:

- **Base**: Atributos comunes (sin ID)
- **Create**: Para POST requests
- **Response**: Para GET requests (incluye ID)

Servicios (Services)
~~~~~~~~~~~~~~~~~~~~

Lógica de negocio:

- Validación de duplicados
- Control de transacciones
- Gestión de stock
- Búsquedas especializadas

Repositorios (Repositories)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Acceso a datos con métodos:

- `create()`: Inserción simple
- `create_with_*()`: Inserción con relaciones
- `get_by_id()`: Búsqueda por ID
- `get_all()`: Listar todos
- `update()`: Actualización
- `delete()`: Eliminación
- Métodos especializados (ej: `get_by_fecha()`)

Convenciones
------------

Nombres de Variables
~~~~~~~~~~~~~~~~~~~~

- `db`: Sesión SQLAlchemy
- `service`: Instancia del servicio
- `data`: Datos del request (esquema Pydantic)
- `id`: Identificador único
- `resultado`: Resultado de operación CRUD

Respuestas HTTP
~~~~~~~~~~~~~~~

- **201**: Creación exitosa
- **200**: Operación exitosa
- **404**: Recurso no encontrado
- **400**: Validación fallida
- **500**: Error del servidor

Control de Stock
~~~~~~~~~~~~~~~~

El sistema maneja stock con:

- Lock a nivel de fila (`FOR UPDATE`) en PostgreSQL
- Validación antes de crear VentaProducto
- Decrementación automática al vender
