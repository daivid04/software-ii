# Refactorización Autoparte - DDD con Lenguaje Ubicuo

## backend/repositories/autoparte_repo.py
| Antes | Después |
|-------|---------|
| `create()` | `registrar_autoparte()` |
| `get_all()` | `listar_catalogo_autopartes()` |
| `get_by_id()` | `consultar_autoparte()` |
| `get_by_name()` | `buscar_autoparte_por_nombre()` |
| `update()` | `actualizar_autoparte()` |
| `delete()` | `dar_de_baja_autoparte()` |
| `get_by_modelo()` | `buscar_autopartes_por_modelo()` |
| `get_by_anio()` | `buscar_autopartes_por_anio()` |

## backend/services/autoparte_service.py
| Antes | Después |
|-------|---------|
| `create_autoparte()` | `registrar_nueva_autoparte()` |
| `list_autopartes()` | `obtener_catalogo_completo()` |
| `get_by_id()` | `consultar_autoparte_disponible()` |
| `get_by_name()` | `buscar_autoparte_por_nombre()` |
| `update_autoparte()` | `actualizar_informacion_autoparte()` |
| `delete_autoparte()` | `dar_de_baja_autoparte()` |
| `get_by_modelo()` | `buscar_autopartes_por_modelo()` |
| `get_by_anio()` | `buscar_autopartes_por_anio()` |

## backend/api/v1/routes/autoparte_routes.py
| Antes | Después |
|-------|---------|
| `create_autoparte()` | `registrar_nueva_autoparte()` |
| `list_autopartes()` | `obtener_catalogo_completo()` |
| `get_autoparte()` | `consultar_autoparte_disponible()` |
| `update_autoparte()` | `actualizar_informacion_autoparte()` |
| `delete_autoparte()` | `dar_de_baja_autoparte()` |
| `get_autopartes_by_modelo()` | `buscar_autopartes_por_modelo()` |
| `get_autopartes_by_anio()` | `buscar_autopartes_por_anio()` |

---
✅ **Validación:** 0 errores en los 3 archivos refactorizados
