# Plan de Asignación de Tareas - Inventario de ICs MVP v1.1
## Sistema Taller de Diego - Arquitectura Hexagonal DDD

**Objetivo General:** Completar el inventario de Ítems de Configuración identificando **mínimo 30-35 ICs** distribuidos en 6 equipos especializados.

**Sistema:** Taller Diego (Gestión de Autopartes, Órdenes, Empleados, Servicios, Ventas, Productos)  
**Arquitectura:** Hexagonal + DDD (6 Bounded Contexts)  
**Tecnología:** FastAPI + SQLAlchemy + Vanilla JS + TailwindCSS

**Formato de Entrega:** Cada equipo completa su tabla y envía al Tech Lead para consolidar.

---

## 📋 Estructura de Tareas

| Tarea | Responsable |
|-------|-------------|
| **T1** | Adriana |
| **T2** |Russell | 
| **T3** | Jarem | 
| **T4** | Percy |
| **T4b** | David | 
| **T5** | Josué | 
| **T6** |  | Tests |

---

## ✅ TAREA 1: Backend Core + Autenticación

**Responsable:** Adriana  
**Componentes:** FastAPI App, Authentication, Database ORM, Health Check  
**Ubicaciones:**
```
backend/main.py                          # Punto de entrada FastAPI
backend/src/auth/                        # Bounded Context: Autenticación
backend/db/base.py                       # ORM Base
backend/db/models/__init__.py            # Importaciones centrales ORM
backend/db/status_routes.py              # Health Check
backend/core/config.py                   # Configuración centralizada
```

## ✅ TAREA 2: Bounded Context - Órdenes + Servicios

**Responsable:** Russell  
**Bounded Contexts:** Operaciones del Taller (Órdenes + Servicios como sub-contexto)  
**Descripción:** Orquesta órdenes de trabajo, servicios, tiempos de garantía, asignación de mecánicos.  
**Ubicaciones:**
```
backend/src/ordenes/
  ├── application/
  ├── domain/
  └── infrastructure/

backend/src/servicios/
  ├── application/
  ├── domain/
  └── infrastructure/
```


## ✅ TAREA 3: Bounded Context - Inventario (Autopartes + Productos)

**Responsable:** Jarem
**Bounded Contexts:** Catálogo e Inventario (Productos base + Autopartes especializadas)  
**Descripción:** Gestión del inventario, alertas de stock, reglas de compatibilidad vehicular.  
**Ubicaciones:**
```
backend/src/producto/
  ├── application/
  ├── domain/
  └── infrastructure/

backend/src/autopartes/
  ├── application/
  ├── domain/
  └── infrastructure/
```
---

## ✅ TAREA 4: Bounded Context - Operaciones (Empleados + Ventas)

**Responsable:** Percy 
**Bounded Contexts:** Gestión de Personal (Empleados) + Transacciones Comerciales (Ventas)  
**Descripción:** Gestión de mecánicos/técnicos + ventas directas de productos al mostrador.  
**Ubicaciones:**
```
backend/src/empleados/
  ├── application/
  ├── domain/
  └── infrastructure/

backend/src/ventas/
  ├── application/
  ├── domain/
  └── infrastructure/
```


---

## ✅ TAREA 4b: Frontend - Interfaz de Usuario

**Responsable:** David
**Componentes:** Vistas HTML, Scripts modulares, Componentes UI, Data Manager  
**Descripción:** Single Page Application con múltiples contextos (Dashboard, Inventario, Órdenes, Servicios)  
**Ubicaciones:**
```
frontend/views/          # Vistas HTML (7 + includes)
  ├── index.html        # Dashboard
  ├── inventory.html    # Gestión de productos
  ├── orden.html        # Gestión de órdenes
  ├── service.html      # Gestión de servicios
  ├── login.html        # Autenticación
  └── includes/         # Componentes reutilizables

frontend/scripts/       # Lógica JavaScript
  ├── main.js          # Inicialización del dashboard
  ├── inventory.js     # Gestión de inventario
  ├── orden.js         # Gestión de órdenes
  ├── service.js       # Gestión de servicios
  ├── login.js         # Autenticación
  ├── data-manager.js  # Gestor centralizado de API
  └── componets/       # Componentes modularizados
```

## ✅ TAREA 5: Infraestructura y DevOps

**Responsable:** Josué 
**Componentes:** Docker, Orquestación, Configuración, Base de Datos  
**Descripción:** Contenerización, CI/CD, variables de entorno, nginx.  
**Ubicaciones:**
```
nginx-optimization.conf          # Reverse proxy
backend/core/config.py           # Configuración centralizada
backend/core/cache.py            # Estrategia de caché distribuido
backend/requirements.txt          # Dependencias Python
backend/.env.prod                # Variables de entorno (secretos)
```

---

## ✅ TAREA 6: Testing, Documentación y Quality Assurance

**Responsable:** QA Lead + Documentation Lead  
**Componentes:** Planes de testing, suites de pruebas, documentación técnica  
**Descripción:** Testing caja negra, integración, unitario + documentación de arquitectura y despliegue.  
**Ubicaciones:**
```
backend/tests/
  ├── caja_negra/              # Testing de API (routes)
  ├── integration/             # Testing entre módulos
  ├── unit/                    # Testing unitario (domain)
  └── mutacion/                # Testing de mutantes


```