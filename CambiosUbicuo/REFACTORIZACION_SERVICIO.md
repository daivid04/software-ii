# Refactorización Servicio - DDD con Lenguaje Ubicuo

## backend/repositories/servicio_repo.py
| Antes | Después |
|-------|---------|
| `create()` | `registrar_servicio()` |
| `get_all()` | `listar_catalogo_servicios()` |
| `get_by_id()` | `consultar_servicio()` |
| `get_by_name()` | `buscar_servicio_por_nombre()` |
| `update()` | `actualizar_servicio()` |
| `delete()` | `dar_de_baja_servicio()` |

## backend/services/servicio_service.py
| Antes | Después |
|-------|---------|
| `create_servicio()` | `registrar_nuevo_servicio()` |
| `list_servicios()` | `obtener_catalogo_completo()` |
| `get_by_id()` | `consultar_servicio_disponible()` |
| `get_by_name()` | `buscar_servicio_por_nombre()` |
| `update_servicio()` | `actualizar_informacion_servicio()` |
| `delete_servicio()` | `dar_de_baja_servicio()` |

## backend/api/v1/routes/servicio_routes.py
| Antes | Después |
|-------|---------|
| `create_servicio()` | `registrar_nuevo_servicio()` |
| `list_servicios()` | `obtener_catalogo_completo()` |
| `get_servicio()` | `consultar_servicio_disponible()` |
| `update_servicio()` | `actualizar_informacion_servicio()` |
| `delete_servicio()` | `dar_de_baja_servicio()` |

---
✅ **Validación:** 0 errores en los 3 archivos refactorizados
