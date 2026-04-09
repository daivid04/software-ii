# 📊 Sistema de Código de Barras Base-26

## Formato: `T-A001-FIL`

### Estructura:
```
T - A001 - FIL
│   │ │    │
│   │ │    └─ Código de categoría (3 letras)
│   │ └────── Número secuencial (001-999)
│   └──────── Letra(s) base-26 (A-ZZ)
└──────────── Prefijo del taller
```

## 🎯 Capacidad

**675,999 combinaciones únicas**

```
A001 - A999    →  999 productos
B001 - Z999    →  25 × 999 = 24,975 productos
AA001 - AZ999  →  26 × 999 = 25,974 productos
BA001 - ZZ999  →  650 × 999 = 649,350 productos
```

## 📝 Ejemplos

| ID | Código | Descripción |
|----|--------|-------------|
| 1 | `T-A001-FIL` | Primer producto |
| 999 | `T-A999-ACE` | Último de letra A |
| 1,000 | `T-B001-LLA` | Inicio letra B |
| 25,974 | `T-Z999-FRE` | Último letra simple |
| 25,975 | `T-AA001-FIL` | Inicio letra doble |
| 675,999 | `T-ZZ999-REP` | Límite máximo |

## 🔧 Implementación

### Archivo: `frontend/scripts/componets/modal-product/modal-event.js`

**Función principal:**
```javascript
generateBarcode(categoria, lastId, existingBarcodes)
```

**Función de conversión:**
```javascript
convertToBase26(num) // Convierte número a formato A001-ZZ999
```

**Lógica:**
```javascript
totalNumber = lastId + 1
letterIndex = (totalNumber - 1) / 999 (división entera)
numberPart = ((totalNumber - 1) % 999) + 1
```

## 📋 Categorías

| Categoría | Código | Categoría | Código |
|-----------|--------|-----------|--------|
| Filtros | FIL | Herramientas | HER |
| Aceites | ACE | Repuestos | REP |
| Llantas | LLA | Accesorios | ACC |
| Baterías | BAT | Iluminación | ILU |
| Frenos | FRE | Eléctricos | ELE |
| Lubricantes | LUB | Suspensión | SUS |
| Motor | MOT | Transmisión | TRA |
| Refrigeración | REF | Combustible | COM |

## ✅ Características

- ✅ **Generación automática** con verificación de unicidad
- ✅ **Compatible CODE128** (ASCII 0-127)
- ✅ **Visualización en modal** con JsBarcode
- ✅ **Descarga PNG** con nombre del producto
- ✅ **Canvas dinámico** ajustado al ancho del código
- ✅ **100 intentos** de generación antes de fallback
- ✅ **Logs detallados** en consola

## 📊 Archivos del Sistema

```
frontend/
├── scripts/
│   ├── utils/
│   │   └── codbarra.js              # Utilidades de generación
│   └── componets/
│       └── modal-product/
│           ├── modal-event.js       # Lógica de generación
│           └── modal-template.js    # UI del código
└── views/
    └── inventory.html               # JsBarcode CDN
```

---

**Versión**: 3.0 (Base-26 Alfanumérica)  
**Última actualización**: 25 de noviembre de 2025

