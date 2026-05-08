# ARQUITECTURA HEXAGONAL - MÓDULO EMPLEADO

## Estructura

```
hexagonal/
├── ports/                          # PUERTOS (Interfaces)
│   ├── employee_driven_port.py    # Puerto Secundario (Driven Port)
│   └── employee_driving_ports.py  # Puertos Primarios (Driving Ports)
│
├── adapters/                       # ADAPTADORES (Implementaciones)
│   ├── secondary/
│   │   └── sqlalchemy_employee_repository.py  # Adaptador Secundario
│   └── primary/
│       └── employee_api_adapter.py            # Adaptador Primario
│
└── usecases/                       # CASOS DE USO (Lógica de negocio)
    └── employee_usecase.py         # Implementa puertos primarios, usa puerto secundario
```

## Componentes Explicados

### 1. PUERTOS SECUNDARIOS (Driven Ports)
**Archivo:** `ports/employee_driven_port.py`

Define la interfaz que la aplicación necesita del mundo externo (base de datos).
- `EmployeeRepository`: Interface con métodos create, get_all, get_by_id, get_by_name, update, delete

```python
class EmployeeRepository(ABC):
    @abstractmethod
    def create(self, employee_data: Dict) -> Dict: ...
    @abstractmethod
    def get_all(self) -> List[Dict]: ...
    # ... otros métodos
```

### 2. PUERTOS PRIMARIOS (Driving Ports)
**Archivo:** `ports/employee_driving_ports.py`

Define los casos de uso que la aplicación expone al mundo externo.
- `CreateEmployeePort`: Crear empleado
- `ListEmployeesPort`: Listar empleados
- `GetEmployeePort`: Obtener por ID
- `UpdateEmployeePort`: Actualizar empleado
- `DeleteEmployeePort`: Eliminar empleado

```python
class CreateEmployeePort(ABC):
    @abstractmethod
    def create_employee(self, employee_data: Dict) -> Dict: ...
```

### 3. ADAPTADORES SECUNDARIOS (Driven Adapters)
**Archivo:** `adapters/secondary/sqlalchemy_employee_repository.py`

Implementa el puerto secundario usando SQLAlchemy.
- Convierte operaciones de dominio en queries SQL
- Traduce modelos ORM (Empleado) a diccionarios

```python
class SqlAlchemyEmployeeRepository(EmployeeRepository):
    def create(self, employee_data: Dict) -> Dict:
        empleado = Empleado(**employee_data)
        self.db.add(empleado)
        self.db.commit()
        return self._to_dict(empleado)
```

### 4. ADAPTADORES PRIMARIOS (Driving Adapters)
**Archivo:** `adapters/primary/employee_api_adapter.py`

Expone los casos de uso mediante API REST (FastAPI).
- Define endpoints HTTP que invocan el caso de uso
- Maneja autenticación, validaciones y errores HTTP

```python
@router.post("/")
def create_empleado(data: EmpleadoCreate, usecase: EmployeeUseCase = Depends(...)):
    return usecase.create_employee(data.model_dump())
```

### 5. CASOS DE USO (Use Cases)
**Archivo:** `usecases/employee_usecase.py`

Contiene la lógica de negocio central.
- Implementa todos los puertos primarios
- Depende del puerto secundario (inyectado)
- Encapsula reglas de negocio (ej: validar nombres únicos)

```python
class EmployeeUseCase(CreateEmployeePort, ListEmployeesPort, ...):
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository
    
    def create_employee(self, employee_data: Dict) -> Dict:
        if self.repository.get_by_name(employee_data.get("nombres")):
            raise ValueError("Ya existe...")
        return self.repository.create(employee_data)
```

## Flujo de Datos (Hexagonal)

```
┌──────────────┐
│  Cliente     │ (Externa)
│  HTTP Request│
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────┐
│ ADAPTADOR PRIMARIO (FastAPI Route)   │ ◄─── Driving Adapter
│ employee_api_adapter.py              │      (cómo invocamos)
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ PUERTO PRIMARIO (Interface)          │ ◄─── Driving Port
│ CreateEmployeePort, ListEmployeesPort│      (qué podemos hacer)
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ CASO DE USO (Lógica de negocio)      │ ◄─── Use Case
│ EmployeeUseCase                      │      (la lógica central)
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ PUERTO SECUNDARIO (Interface)        │ ◄─── Driven Port
│ EmployeeRepository                   │      (qué necesitamos)
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│ ADAPTADOR SECUNDARIO (SQLAlchemy)    │ ◄─── Driven Adapter
│ SqlAlchemyEmployeeRepository         │      (cómo persistimos)
└──────┬───────────────────────────────┘
       │
       ▼
┌──────────────┐
│ Base de Datos│ (Externa)
└──────────────┘
```

## Cómo Integrar en main.py

En `backend/main.py`, agregar:

```python
from fastapi import FastAPI
from hexagonal.adapters.primary.employee_api_adapter import router as employee_router

app = FastAPI()

# Incluir las routes hexagonales de empleado
app.include_router(employee_router, prefix="/api/v1/empleados", tags=["Empleados"])
```

## Ventajas de esta arquitectura

1. **Independencia de tecnología**: Cambiar de SQLAlchemy a otra BD es simple (solo cambiar adaptador)
2. **Testeable**: Puertos secundarios pueden ser mocks para tests
3. **Mantenible**: La lógica de negocio está centralizada en el caso de uso
4. **Escalable**: Agregar nuevos adaptadores (primarios o secundarios) sin afectar el caso de uso
5. **Separación de responsabilidades**: Cada componente tiene un rol claro

## Notas

- La lógica del caso de uso es idéntica a la del `EmpleadoService` original, solo restructurada
- Los puertos definen "qué" podemos hacer (interfaces)
- Los adaptadores definen "cómo" lo hacemos (implementaciones)
- El caso de uso define "por qué" lo hacemos (reglas de negocio)
