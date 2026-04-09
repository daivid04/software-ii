# Seguridad contra XSS (Cross-Site Scripting)

## 🛡️ Protecciones Implementadas

Este documento describe las medidas de seguridad implementadas para prevenir ataques de inyección de scripts (XSS).

## 📋 Índice

1. [Frontend - Sanitización](#frontend---sanitización)
2. [Backend - Validación](#backend---validación)
3. [Pruebas de Seguridad](#pruebas-de-seguridad)
4. [Buenas Prácticas](#buenas-prácticas)

---

## Frontend - Sanitización

### Utilidad de Sanitización (`utils/sanitize.js`)

Se creó una utilidad central para escapar caracteres HTML peligrosos:

```javascript
export function escapeHtml(value) {
  if (value === null || value === undefined) {
    return '';
  }

  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
    .replace(/\//g, '&#x2F;');
}
```

### Archivos Protegidos

#### 1. **product-card.js**
- ✅ Sanitiza: nombre, descripción, precios, stock
- ✅ Escapa atributos HTML (data-product-id, data-id)

#### 2. **notification.js**
- ✅ Usa `textContent` en lugar de `innerHTML`
- ✅ Previene ejecución de scripts en notificaciones

#### 3. **service.js**
- ✅ Sanitiza: nombre, descripción de servicios
- ✅ Escapa datos en templates HTML

#### 4. **orden.js**
- ✅ Sanitiza: nombres de productos, cantidades, precios
- ✅ Escapa datos en tablas y dropdowns

---

## Backend - Validación

### Validadores Pydantic

Se implementaron validadores en los schemas para eliminar HTML/scripts antes de guardar en BD.

#### producto_schema.py

```python
from pydantic import BaseModel, field_validator
import re

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    marca: str
    categoria: str
    
    @field_validator('nombre', 'descripcion', 'marca', 'categoria')
    @classmethod
    def sanitize_html(cls, v: str) -> str:
        """Prevenir inyección de scripts HTML/JavaScript"""
        if v is None:
            return v
        # Eliminar tags HTML y scripts
        v = re.sub(r'<[^>]*>', '', v)
        # Eliminar caracteres peligrosos
        v = re.sub(r'[<>"\'"]', '', v)
        return v.strip()
```

#### Schemas Protegidos

- ✅ `producto_schema.py` - Productos
- ✅ `servicio_schema.py` - Servicios
- ✅ `autoparte_schema.py` - Autopartes

---

## Pruebas de Seguridad

### Caso de Prueba: Inyección de Scripts

**Input malicioso:**
```html
<script>alert('XSS')</script>
<img src=x onerror="alert('XSS')">
"><script>alert(String.fromCharCode(88,83,83))</script>
```

**Resultado Esperado:**

1. **Backend:**
   - El script se elimina antes de guardar
   - Se guarda como: `scriptalert('XSS')script` (sin tags)

2. **Frontend:**
   - Si se recibe con tags, se muestra como texto plano
   - Se renderiza como: `&lt;script&gt;alert('XSS')&lt;/script&gt;`
   - **NO se ejecuta el código**

### Pruebas Automatizadas

```bash
# Crear producto con XSS
curl -X POST http://localhost:8000/api/v1/productos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "<script>alert(\"XSS\")</script>",
    "descripcion": "<img src=x onerror=\"alert(1)\">",
    "marca": "Test",
    "categoria": "Test",
    "precioCompra": 100,
    "precioVenta": 150,
    "stock": 10,
    "stockMin": 5
  }'

# Verificar que se guardó sin tags peligrosos
curl http://localhost:8000/api/v1/productos/
```

### Prueba Manual en Frontend

1. Ir a Inventario
2. Agregar producto con nombre: `<script>alert('hola')</script>`
3. Guardar
4. **Verificar:**
   - ✅ No se ejecuta ningún alert
   - ✅ El nombre se muestra como texto plano
   - ✅ En la BD se guardó sin los tags `<script>`

---

## Buenas Prácticas

### ✅ DO (Hacer)

1. **Usar `escapeHtml()` para datos de usuario**
   ```javascript
   element.innerHTML = `<div>${escapeHtml(userData)}</div>`;
   ```

2. **Preferir `textContent` sobre `innerHTML`**
   ```javascript
   element.textContent = userData; // Seguro
   ```

3. **Validar en Backend y Frontend**
   - Backend: Validadores Pydantic
   - Frontend: Sanitización antes de renderizar

4. **Escapar atributos HTML**
   ```javascript
   `<div data-name="${escapeHtml(name)}">`
   ```

### ❌ DON'T (No hacer)

1. **NO usar `innerHTML` directamente con datos de usuario**
   ```javascript
   // ❌ PELIGROSO
   element.innerHTML = userData;
   ```

2. **NO confiar solo en validación frontend**
   - Siempre validar en backend

3. **NO permitir HTML en campos de texto**
   - Usar plain text
   - Para rich text, usar librerías especializadas (DOMPurify)

4. **NO usar `eval()` o `Function()` con datos de usuario**
   ```javascript
   // ❌ NUNCA HACER ESTO
   eval(userData);
   ```

---

## Capas de Defensa

```
┌─────────────────────────────────────┐
│  1. Validación de Input (Frontend)  │
│     - Tipos de campo correctos      │
│     - Límites de caracteres         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. Sanitización (Frontend)         │
│     - escapeHtml() en renderizado   │
│     - textContent vs innerHTML      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  3. Validación Backend (Pydantic)   │
│     - field_validator()             │
│     - Regex para eliminar tags      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  4. Base de Datos                   │
│     - Datos ya sanitizados          │
│     - Sin scripts ejecutables       │
└─────────────────────────────────────┘
```

---

## Reporte de Vulnerabilidades

Si encuentras una vulnerabilidad de seguridad:

1. **NO la publiques públicamente**
2. Reporta al equipo de desarrollo
3. Incluye:
   - Pasos para reproducir
   - Impacto potencial
   - Sugerencias de solución

---

## Referencias

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [MDN: textContent vs innerHTML](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)

---

**Última actualización:** Diciembre 4, 2025
**Estado:** ✅ Protecciones activas en producción
