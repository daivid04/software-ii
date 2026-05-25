# Plan de Pruebas Automatizadas v1 (Test_Plan_v1.md)

Este documento define la estrategia, estructura, alcance y criterios de aceptación del ecosistema de pruebas automatizadas implementado para el Sistema de Gestión de Taller Automotriz y Almacén de Repuestos. El framework está diseñado siguiendo los principios de **Diseño Guiado por el Dominio (DDD)** y **Arquitectura Hexagonal**, garantizando el aislamiento absoluto del núcleo del negocio frente a dependencias de infraestructura (como PostgreSQL, Redis y frameworks web como FastAPI).

---

## 1. Arquitectura del Ecosistema de Pruebas

Para cumplir con las exigencias métricas y de aislamiento de la guía de laboratorio, la suite se organiza de manera lineal y desacoplada, utilizando **Pytest** como motor de ejecución principal y **Coverage.py** para la auditoría de cobertura.

```
tests/
│
├── unit/                       # FASE 2: Blindaje Puro del Dominio
│   ├── test_value_objects.py   # Inmutabilidad, validaciones atómicas e invariantes base
│   ├── test_empleado_domain.py # Reglas de estado de personal
│   ├── test_orden_domain.py    # Orquestación de mecánicos, servicios y garantías
│   ├── test_producto_domain.py # Control estricto de existencias e invariantes de precios
│   ├── test_autoparte_domain.py# Compatibilidad y herencia táctica de productos
│   ├── test_venta_domain.py    # Consistencia del agregado raíz de transacciones
│   └── test_servicio_domain.py # Reglas de información y sanitización de servicios
│
├── integration/                # FASE 4: Ensamblaje y Orquestación (Application Services)
│   ├── test_empleado_service.py# Flujo de personal, control de duplicados e invalidación de caché
│   ├── test_orden_service.py   # Consistencia transaccional compleja (El Jefe Final)
│   ├── test_producto_service.py# Actualizaciones de inventario y estado
│   ├── test_autoparte_service.py# Persistencia falsa con datos heredados y compatibilidad
│   ├── test_venta_service.py    # Consistencia inter-agregado (Ventas -> Descuento Stock)
│   └── test_servicio_service.py # Validación y persistencia de catálogos operativos
│
└── mocks/                      # FASE 3: Simulacro y Puertos en Memoria
    └── fake_repos.py           # Repositorios falsos que operan sobre listas en memoria RAM
```

---

## 2. Bounded Contexts (Contextos Delimitados) Involucrados

El sistema se divide en cuatro Contextos Delimitados claros, cuyos límites de consistencia han sido protegidos mediante las pruebas automatizadas:

1. **Contexto de Gestión de Personal (Módulo Empleados):** Gobierna el ciclo de vida de los mecánicos y técnicos, sus especialidades y sus estados de disponibilidad (`activo`, `inactivo`).
2. **Contexto de Inventario y Catálogo (Módulos Productos y Autopartes):** Controla las existencias físicas del almacén, las alertas de stock mínimo, los márgenes de ganancias mediante invariantes de precio, y las reglas específicas de compatibilidad vehicular para repuestos (Autopartes).
3. **Contexto de Operaciones del Taller (Módulos Órdenes y Servicios):** Orquesta las órdenes de trabajo, los tiempos de garantía aplicados a reparaciones, el cálculo del costo operativo del servicio y la asignación de mecánicos idóneos.
4. **Contexto de Transacciones Comerciales (Módulo Ventas):** Administra las salidas financieras rápidas de repuestos o productos de mostrador directas al cliente, exigiendo consistencia en tiempo real con el inventario.

---

## 3. Fase 2: Blindaje — Pruebas Unitarias del Dominio

Las pruebas unitarias evalúan componentes puros del dominio (clases estándar de Python con `@dataclass`), sin inicializar el motor ORM (SQLAlchemy) ni establecer conexiones de red.

### 3.1. Pruebas de Objetos de Valor (Value Objects)
Se verifica que los Value Objects actúen como bloques constructivos inmutables, se comparen únicamente por sus atributos internos y carezcan de una identidad propia (ID).

* **`PrecioVO` e `InventarioVO`:**
    * *Criterio de Validación:* Bloquear compras o ventas negativas y asegurar que el precio de venta nunca sea inferior al precio de compra (Invariante comercial). Evitar stocks iniciales o mínimos negativos.
* **`InformacionEmpleadoVO` y `EstadoEmpleadoVO`:**
    * *Criterio de Validación:* Validar longitud mínima de nombres, apellidos y obligatoriedad de especialidades. Limitar los estados de personal estrictamente a valores válidos en minúsculas.
* **`GarantiaVO`, `EstadoPagoVO` y `PrecioOrdenVO`:**
    * *Criterio de Validación:* Asegurar que los meses de garantía estén dentro de rangos permitidos (no negativos) y que el precio asignado a una orden de trabajo sea coherente.
* **`CompatibilidadVehiculoVO`:**
    * *Criterio de Validación:* Validar la longitud del modelo del vehículo y el formato de los años de compatibilidad para evitar registros corruptos en repuestos.
* **`CantidadVentaVO` y `FechaVentaVO`:**
    * *Criterio de Validación:* Validar que las transacciones contengan cantidades estrictamente mayores a cero y prohibir transacciones comerciales fechadas en el futuro.

### 3.2. Pruebas de Entidades y Agregados (Cambios de Estado e Invariantes)

* **`EmpleadoDomain`:**
    * *Caso de Prueba:* Cambio de estado y actualización de especialidad.
    * *Invariante:* El cambio de estado debe sanitizarse automáticamente a minúsculas (`ACTIVO` -> `activo`) a través del VO.
* **`ServicioDomain`:**
    * *Caso de Prueba:* Intento de registrar descripciones cortas.
    * *Invariante:* Si la descripción contiene menos de 10 caracteres, el agregado rechaza la mutación lanzando un `ValueError`.
* **`ProductoDomain`:**
    * *Caso de Prueba:* Despacho exitoso versus quiebre de stock.
    * *Invariante:* Al invocar `registrar_despacho()`, si la cantidad solicitada supera al atributo `stock`, la entidad bloquea la operación y mantiene el stock original intacto.
* **`AutoparteDomain`:**
    * *Caso de Prueba:* Asignación de compatibilidad vehicular por herencia.
    * *Invariante:* Valida que los datos del vehículo cumplan con el formato del VO heredando de forma transparente las protecciones de inventario de `ProductoDomain`.
* **`VentaDomain`:**
    * *Caso de Prueba:* Inicialización de fecha y agregación de detalles de artículos.
    * *Invariante:* Rechaza inmediatamente la agregación de productos con cantidades iguales o menores a cero.
* **`OrdenDomain`:**
    * *Caso de Prueba:* Asignación de mecánicos basada en disponibilidad.
    * *Invariante Crítica:* Si un mecánico posee el estado `inactivo`, el método `asignar_empleado()` aborta el proceso, impidiendo que una orden de trabajo sea asignada a personal no disponible.

---

## 4. Fase 3: Simulacro — Aislamiento mediante Arquitectura Hexagonal

Para ejecutar las pruebas del sistema de forma totalmente aislada sin requerir contenedores Docker o servidores locales activos de PostgreSQL y Redis, se implementó el patrón de **Puertos y Adaptadores** a nivel de persistencia y caché.

### 4.1. Repositorios Falsos en Memoria (Fake Repositories)
En lugar de inyectar sesiones reales de SQLAlchemy (`Session`), las clases de la capa de aplicación interactúan con implementaciones falsas que exponen la misma firma e interfaz de operaciones que los repositorios reales, pero almacenan la información dentro de listas mutables nativas de Python (`list`).

Cada repositorio simula de manera transparente operaciones críticas:
* **Auto-incremento:** Generación automatizada de llaves primarias (`id`) numéricas secuenciales al guardar.
* **Búsquedas:** Filtrado mediante generadores de listas para métodos como `buscar_empleado_por_nombre`, `consultar_producto`, etc.
* **Manejo de Referencias:** Mutación de objetos en memoria simulando el comportamiento de confirmación (`commit`) de transacciones de base de datos.

### 4.2. Aislamiento del Estado (Equivalente a `beforeEach`)
En **Pytest**, el aislamiento del estado para evitar que un caso de prueba altere el resultado del siguiente se maneja mediante el uso de **Fixtures** con alcance por función (`scope="function"` por defecto). 

Cada test de integración inyecta una función fixture (ej. `def empleado_service()` o `def orden_service()`) que instancia un repositorio en memoria completamente limpio y vacío justo antes de ejecutar las líneas de código del caso de prueba actual.

---

## 5. Fase 4: Ensamblaje — Pruebas de Integración

Las pruebas de integración evalúan la capa de aplicación (`Application Services`), donde los orquestadores reciben esquemas Pydantic (simulando los cuerpos JSON de las solicitudes HTTP de FastAPI), recuperan datos desde la persistencia, interactúan con las reglas de negocio del Dominio y aplican la lógica de sincronización e invalidación de memoria caché.

### 5.1. Casos de Prueba de Integración Clave

| Módulo / Servicio | Caso de Prueba (Flujo Evaluado) | Evento / Comportamiento de Infraestructura Asociado | Criterio de Validación |
| :--- | :--- | :--- | :--- |
| **`EmpleadoService`** | Registro exitoso de personal nuevo. | Desencadena `cache.invalidate_pattern('empleados')`. | El ID simulado pasa a ser `1` y la caché global del catálogo se invalida. |
| **`EmpleadoService`** | Intento de registro con nombres duplicados. | Consulta previa al repositorio en memoria. | Lanza un `ValueError` preventivo antes de tocar las entidades del dominio. |
| **`EmpleadoService`** | Baja definitiva de un mecánico. | Desencadena `cache.delete(f'empleado_{id}')`. | El objeto es removido de la lista y se limpia su caché llave-valor específica. |
| **`ProductoService`** | Actualización de stock y variación de precios. | Desencadena mutación en el agregado e invalidación parcial de caché. | Modifica stock e invalida de forma atómica la caché de mostrador del producto. |
| **`AutoparteService`** | Registro de repuesto compatible. | Conversión bidireccional mediante métodos `to_domain()` y `from_domain()`. | Mapea con éxito atributos extendidos (`modelo`, `anio`) sobre persistencia falsa. |
| **`VentaService`** | **Consistencia Inter-Agregado:** Venta exitosa de múltiples artículos de mostrador. | Orquestación cruzada: `VentaRepository` y `ProductoRepository`. | Descuenta con total éxito las unidades del stock del producto y guarda la venta. |
| **`VentaService`** | Aborto de venta por quiebre de inventario. | Captura de excepción del dominio y mapeo a error web. | El `ValueError` del dominio se transforma en una excepción HTTP de FastAPI (`HTTPException` con código `400`). La base de datos de ventas permanece intacta. |
| **`OrdenService`** | **Orquestación Compleja:** Registro de orden de trabajo con servicios y mecánicos. | Orquestación de tres repositorios falsos simultáneos y simulación ORM. | Calcula costos, asocia registros de mapeo intermedio y limpia el catálogo de órdenes en caché. |
| **`OrdenService`** | Rechazo de orden por mecánico no disponible. | Bloqueo transaccional inmediato. | Detiene el flujo lanzando un error HTTP `400 Bad Request` indicando que el operario no está activo. Ningún registro se persiste. |
| **`ServicioService`** | Registro y control de duplicados en el catálogo de mano de obra. | Sanitización activa de cadenas de texto y HTML mediante validadores Pydantic. | Registra servicios válidos y bloquea textos descriptivos inválidos o maliciosos. |

---

## 6. Eventos de Dominio Asociados

Aunque la arquitectura actual mantiene una sincronización síncrona mediante servicios de aplicación, los flujos probados mapean directamente la ocurrencia de los siguientes eventos lógicos de negocio:

* **`EmpleadoRegistrado` / `EmpleadoDadoDeBaja`:** Impacta la disponibilidad inmediata de personal en el taller técnico.
* **`OrdenDeTrabajoCreada`:** Evento raíz que amarra los contextos de personal y operaciones de taller, congelando precios cotizados.
* **`VentaConsumada`:** Dispara de forma obligatoria la actualización síncrona en el contexto de inventario, gatillando alertas si el stock resultante es inferior al valor estipulado en `stock_minimo`.
* **`IntentoDeTransaccionInvalida`:** Evento de error crítico que detiene canalizaciones financieras y operativas del taller antes de generar inconsistencias de datos en base de datos.