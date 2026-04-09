Modelos de Base de Datos
==========================

.. py:module:: db.models

Los modelos representan las tablas de la base de datos usando SQLAlchemy ORM.

Productos
---------

.. automodule:: db.models.producto
   :members:
   :undoc-members:
   :show-inheritance:

Autopartes
----------

.. automodule:: db.models.autoparte
   :members:
   :undoc-members:
   :show-inheritance:

Servicios
---------

.. automodule:: db.models.servicio
   :members:
   :undoc-members:
   :show-inheritance:

Empleados
---------

.. automodule:: db.models.empleado
   :members:
   :undoc-members:
   :show-inheritance:

Órdenes
-------

.. automodule:: db.models.orden
   :members:
   :undoc-members:
   :show-inheritance:

Órdenes - Servicios (Junction Table)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: db.models.orden_servicio
   :members:
   :undoc-members:
   :show-inheritance:

Órdenes - Empleados (Many-to-Many)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: db.models.orden_empleado
   :members:
   :undoc-members:
   :show-inheritance:

Ventas
------

.. automodule:: db.models.venta
   :members:
   :undoc-members:
   :show-inheritance:

Ventas - Productos (Line Items)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: db.models.venta_producto
   :members:
   :undoc-members:
   :show-inheritance:
