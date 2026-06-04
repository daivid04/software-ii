# Inventario de Ítems de Configuración (ICs) - MVP v1.1

**Proyecto:** Sistema de Gestión de Autopartes  
**Versión:** MVP v1.1  
**Fecha:** 2026-06-04  
**Estado:** Inicial  

---

## Resumen Ejecutivo

Este documento registra los **Ítems de Configuración** identificados para el MVP v1.1 bajo control formal de Gestión de Configuración del Software (GCS). Incluye 16 ICs distribuidos en 4 categorías estratégicas.

| Categoría | Cantidad | Criticidad Alta |
|-----------|----------|-----------------|
| **Código** | 5 | 4 |
| **Infraestructura** | 4 | 3 |
| **Configuración** | 4 | 4 |
| **Documentación** | 3 | 1 |
| **TOTAL** | **16** | **12** |

---

## Registro de Ítems de Configuración

| ID-IC | Categoría | Nombre | Ubicación | Versión | Responsable | Criticidad | Justificación |
|-------|-----------|--------|-----------|---------|-------------|------------|---------------|
| **CÓDIGO** |
| IC-001 | Código | Servicio de Autenticación | `backend/src/auth/application/` | 1.0.0 | Team Backend | **ALTA** | Bloquea el acceso a toda la plataforma. Su corrupción impide despliegue. |
| IC-002 | Código | ORM de Base de Datos | `backend/db/base.py` | 1.0.0 | Team Backend | **ALTA** | Controlador central de todas las operaciones de BD. Sin él, la compilación falla. |
| IC-003 | Código | Servicio de Órdenes | `backend/src/ordenes/application/` | 1.0.0 | Team Backend | **ALTA** | Core del MVP. Gestiona operaciones críticas de negocio. |
| IC-004 | Código | API REST Principal | `backend/main.py` | 1.0.0 | Team Backend | **ALTA** | Punto de entrada de toda la aplicación backend. |
| IC-005 | Código | Frontend Principal | `frontend/views/index.html` | 1.0.0 | Team Frontend | **ALTA** | Interfaz principal de usuario. Punto de entrada de clientes. |
| **INFRAESTRUCTURA** |
| IC-006 | Infraestructura | Docker Compose Producción | `docker-compose.prod.yml` | 1.0.0 | DevOps | **ALTA** | Orquesta todos los contenedores en producción. Sin él, no hay despliegue. |
| IC-007 | Infraestructura | Dockerfile Backend | `backend/Dockerfile` | 1.0.0 | DevOps | **ALTA** | Define la imagen de contenedor. Cambios rompen la cadena CI/CD. |
| IC-008 | Infraestructura | Configuración Nginx | `nginx-optimization.conf` | 1.0.0 | DevOps | **MEDIA** | Optimización de rendimiento. Su pérdida degrada experiencia de usuario. |
| IC-009 | Infraestructura | Service Worker Frontend | `frontend/service-worker.js` | 1.0.0 | Team Frontend | **MEDIA** | Caché offline y sincronización. Mejora UX pero no bloquea despliegue. |
| **CONFIGURACIÓN** |
| IC-010 | Configuración | Variables de Entorno Producción | `backend/.env.prod` | 1.0.0 | DevOps | **ALTA** | Credenciales, secretos y endpoints críticos. Su corrupción paraliza la plataforma. |
| IC-011 | Configuración | Archivo de Dependencias Python | `requirements.txt` | 1.0.0 | Team Backend | **ALTA** | Especifica todas las librerías. Sin él, compilación imposible. |
| IC-012 | Configuración | Configuración de Base de Datos | `backend/core/config.py` | 1.0.0 | Team Backend | **ALTA** | Configuración de conexión a BD y caché. Crítica para operación. |
| IC-013 | Configuración | Configuración de Cache | `backend/core/cache.py` | 1.0.0 | Team Backend | **MEDIA** | Estrategia de caché distribuido. Su pérdida afecta rendimiento. |
| **DOCUMENTACIÓN** |
| IC-014 | Documentación | Guía de Despliegue | `DEPLOYMENT_GUIDE.md` | 1.0.0 | Tech Lead | **ALTA** | Procedimiento reproducible para despliegues. Crítica para continuidad operativa. |
| IC-015 | Documentación | Estándar de Seguridad XSS | `backend/SEGURIDAD_XSS.md` | 1.0.0 | Security Team | **MEDIA** | Referencia de mitigación. Falta conocimiento crítico pero no rompe compilación. |
| IC-016 | Documentación | Plan de Testing | `backend/tests/Test_Plan_v1.md` | 1.0.0 | QA Lead | **BAJA** | Referencia de cobertura. Informativo; no afecta compilación ni despliegue. |

---

## Criterios de Asignación de Criticidad

### ⛔ CRITICIDAD ALTA (12 ICs)
**Definición:** Su pérdida, corrupción o falta de control **bloquea inmediatamente** la compilación o despliegue.

**Ejemplos del MVP:**
- `IC-001` - Auth bloquea acceso
- `IC-006` - Sin Docker Compose, no hay orquestación
- `IC-010` - Sin variables de entorno, no conecta a servicios externos
- `IC-014` - Sin guía, despliegues son caóticos e irreproducibles

### 🟠 CRITICIDAD MEDIA (3 ICs)
**Definición:** Afecta **funcionalidades importantes** o rendimiento, pero no bloquea compilación/despliegue.

**Ejemplos del MVP:**
- `IC-008` - Nginx: fallos de optimización degradan UX pero sistema sigue operativo
- `IC-009` - Service Worker: offline mode fallido pero usuario accede online
- `IC-013` - Cache: estrategia fallida ralentiza, no impide operación

### 🟢 CRITICIDAD BAJA (1 IC)
**Definición:** Impacto **limitado o documental**. No afecta compilación ni despliegue.

**Ejemplos del MVP:**
- `IC-016` - Test Plan: referencia informativa, cambios no impiden ejecutar tests

---

## Justificación Técnica: ¿Por qué algunos archivos SÍ son ICs y otros NO?

### ✅ `docker-compose.prod.yml` **SÍ es IC** (IC-006)
- **Identificación única:** Archivo crítico y singular en producción
- **Control de cambios necesario:** Cualquier error rompe la orquestación completa
- **Responsable asignado:** DevOps
- **Historial de versiones:** Cada cambio debe ser registrado y auditado
- **Auditoría requerida:** Cambios no autorizados comprometen seguridad

### ❌ `README.md` secundario **NO es IC**
- **Propósito:** Información de bienvenida/orientación
- **Impacto:** Su corrupción no afecta compilación ni despliegue
- **Cambios:** Se puede actualizar sin afectar integridad del producto
- **Control:** No requiere línea base (baseline) formal
- **Auditoría:** No es crítico para reproducibilidad

### ✅ `backend/src/auth/application/` **SÍ es IC** (IC-001)
- **Criticidad:** Bloquea acceso a toda la plataforma
- **Compilación:** Error aquí = compilación fallida
- **Despliegue:** Sin autenticación, MVP no es viable

---

## Baselines Definidas

### Baseline v1.1.0 (Candidato a Producción)

```
Tag: v1.1.0 (firmado)
Fecha: 2026-06-04
Estado: En validación

ICs Congelados:
- Todos los 16 ICs en versión 1.0.0
- Commit hash: [hash principal]

Punto de referencia reproducible:
git checkout v1.1.0
```

---

## Próximos Pasos

1. **Revisión de Stakeholders:** QA, DevOps, Tech Lead
2. **Validación de Baselines:** Verificar reproducibilidad
3. **Asignación de Responsables:** Confirmar ownership de cada IC
4. **Control de Cambios:** Implementar workflow CCB (Change Control Board)
5. **Auditoría Inicial:** Verificar trazabilidad histórica en Git

---

## Referencias

- **IEEE 828-2012:** Standard for Configuration Management
- **SWEBOK v4.0a:** Software Configuration Management (KA)
- **Pro Git (Cap. 2-3):** Chacon & Straub, 2014

---

**Documento:** Inventario de ICs MVP v1.1  
**Última actualización:** 2026-06-04  
**Próxima revisión:** 2026-07-04
