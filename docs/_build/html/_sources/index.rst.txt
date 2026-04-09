Backend API Documentation
==========================

Índice de Contenidos
--------------------

.. toctree::
   :maxdepth: 2
   :caption: Módulos Backend

   modules/models
   modules/schemas
   modules/repositories
   modules/services
   modules/routes

.. toctree::
   :maxdepth: 1
   :caption: Información General

   intro
   architecture

Introducción
------------

Esta es la documentación del backend de **Taller Diego**, un sistema de gestión de órdenes de servicio, ventas y autopartes.

El proyecto utiliza:

- **FastAPI** para los endpoints REST
- **SQLAlchemy** como ORM
- **PostgreSQL** (Supabase) como base de datos
- **Pydantic** para validación de esquemas

Arquitectura
~~~~~~~~~~~~

El proyecto sigue una arquitectura de **N capas**:

1. **Routes** (API REST) → Endpoints FastAPI
2. **Services** (Lógica de negocio) → Validaciones y procesamiento
3. **Repositories** (Acceso a datos) → Operaciones CRUD
4. **Models** (Modelos de BD) → Entidades SQLAlchemy
5. **Schemas** (Validación) → Modelos Pydantic

.. image:: ../_static/architecture.png
   :alt: Arquitectura del Proyecto
   :align: center

Quick Links
-----------

- :doc:`modules/models` - Modelos de Base de Datos
- :doc:`modules/services` - Servicios de Negocio
- :doc:`modules/routes` - Endpoints API
- GitHub: https://github.com/ESIS-DevTeam/Taller-Diego
