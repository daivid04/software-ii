# Refactorización Orden - DDD con Lenguaje Ubicuo

## backend/repositories/orden_repo.py
| Antes | Después |
|-------|---------|
| `create()` | `registrar_orden()` |
| `create_with_services()` | `registrar_orden_con_servicios()` |
| `get_all()` | `listar_catalogo_ordenes()` |
| `get_by_id()` | `consultar_orden()` |
| `delete()` | `dar_de_baja_orden()` |
| `get_by_fecha()` | `consultar_ordenes_por_fecha()` |

## backend/services/orden_service.py
| Antes | Después |
|-------|---------|
| `create_orden()` | `registrar_nueva_orden()` |
| `list_ordens()` | `obtener_catalogo_completo()` |
| `get_by_id()` | `consultar_orden()` |
| `get_by_fecha()` | `consultar_ordenes_por_fecha()` |
| `delete_orden()` | `dar_de_baja_orden()` |

## backend/api/v1/routes/orden_routes.py
| Antes | Después |
|-------|---------|
| `create_orden()` | `registrar_nueva_orden()` |
| `list_ordens()` | `obtener_catalogo_completo()` |
| `get_orden_by_id()` | `consultar_orden()` |
| `get_ordens_by_fecha()` | `consultar_ordenes_por_fecha()` |
| `delete_orden()` | `dar_de_baja_orden()` |

---
✅ **Validación:** 0 errores en los 3 archivos refactorizados
