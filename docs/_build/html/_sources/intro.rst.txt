intro
=====

Introducción General
--------------------

Este proyecto es un sistema completo de gestión para un taller mecánico.

Características principales:

- Gestión de productos y autopartes
- Control de órdenes de servicio
- Registro de ventas
- Control de empleados
- Gestión de stock
- API REST con FastAPI

Requisitos
----------

- Python 3.9+
- PostgreSQL 13+
- pip o poetry

Instalación
-----------

.. code-block:: bash

    # Clonar repositorio
    git clone https://github.com/ESIS-DevTeam/Taller-Diego.git
    cd Taller-Diego

    # Instalar dependencias
    pip install -r requirements.txt

    # Ejecutar servidor
    python backend/main.py

La API estará disponible en ``http://localhost:8000``

Documentación Interactiva
~~~~~~~~~~~~~~~~~~~~~~~~~

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Endpoints Principales
---------------------

Productos
~~~~~~~~~

- ``POST /productos`` - Crear producto
- ``GET /productos`` - Listar productos
- ``GET /productos/{id}`` - Obtener producto
- ``PUT /productos/{id}`` - Actualizar producto
- ``DELETE /productos/{id}`` - Eliminar producto

Órdenes
~~~~~~~

- ``POST /ordenes`` - Crear orden
- ``GET /ordenes`` - Listar órdenes
- ``GET /ordenes/{id}`` - Obtener orden
- ``DELETE /ordenes/{id}`` - Eliminar orden

Ventas
~~~~~~

- ``POST /ventas`` - Crear venta
- ``GET /ventas`` - Listar ventas
- ``GET /ventas/{id}`` - Obtener venta
- ``DELETE /ventas/{id}`` - Eliminar venta

Health Check
~~~~~~~~~~~~

- ``GET /`` - Valida conectividad Backend ↔ Database

Generación de Documentación HTML
---------------------------------

.. code-block:: bash

    cd docs
    sphinx-build -b html . _build/html

La documentación estará en ``docs/_build/html/index.html``
