# Guía de Despliegue - Optimizaciones de Rendimiento

## 📋 Resumen de Cambios

Se han implementado optimizaciones en 3 capas que reducirán el tiempo de carga de **5 segundos a < 1 segundo**:

### Backend
- ✅ Caché en memoria con TTL de 5 minutos
- ✅ Compresión gzip automática
- ✅ Headers de caché para API responses

### Frontend
- ✅ Caché en localStorage con TTL
- ✅ Skeleton loaders para mejor UX
- ✅ Renderizado optimizado con DocumentFragment
- ✅ Service Worker para caché offline

### Servidor
- ✅ Configuración de Nginx optimizada

---

## 🚀 Pasos de Despliegue

### 1. Desplegar Backend

```bash
# SSH a tu VPS
ssh usuario@tu-vps-ip

# Navegar al directorio del backend
cd /var/www/tallerDiego_backend

# Hacer pull de los cambios
git pull origin main

# Reiniciar el servicio
sudo systemctl restart taller-diego-backend
# O si usas uvicorn directamente:
# pkill -f uvicorn && uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### 2. Desplegar Frontend

```bash
# En el mismo servidor, navegar al frontend
cd /var/www/tallerDiego_frontend

# Hacer pull de los cambios
git pull origin main

# Copiar el service worker a la raíz del sitio
cp service-worker.js /var/www/tallerDiego_frontend/
```

### 3. Configurar Nginx

```bash
# Copiar la configuración de optimización
sudo cp /var/www/tallerDiego_frontend/nginx-optimization.conf /etc/nginx/conf.d/taller-diego-optimization.conf

# O si prefieres, agregar las configuraciones a tu archivo de sitio existente
sudo nano /etc/nginx/sites-available/taller-diego

# Verificar la configuración
sudo nginx -t

# Si todo está bien, recargar Nginx
sudo systemctl reload nginx
```

### 4. Verificar Despliegue

```bash
# Verificar que el backend esté corriendo
curl http://localhost:8000/api/v1/productos/

# Verificar compresión gzip
curl -H "Accept-Encoding: gzip" -I http://tu-vps-ip/api/v1/productos/

# Verificar headers de caché
curl -I http://tu-vps-ip/styles/css/inventory.css
```

---

## 🧪 Testing de Performance

### Desde tu navegador:

1. **Abrir DevTools** (F12)
2. **Network Tab** → Limpiar caché (Ctrl+Shift+Delete)
3. **Recargar página** con Network throttling "Fast 3G"
4. **Verificar métricas:**
   - First Contentful Paint < 1s
   - Skeleton loaders aparecen inmediatamente
   - Datos cargan en < 500ms (segunda carga)

### Verificar caché:

```bash
# En DevTools Console:
localStorage.getItem('api_cache_productos')
# Debería mostrar los datos cacheados

# Verificar Service Worker:
navigator.serviceWorker.getRegistrations()
# Debería mostrar el service worker registrado
```

### Lighthouse Test:

```bash
# Desde tu máquina local
npx lighthouse http://tu-vps-ip/views/inventory.html --view
```

**Métricas esperadas:**
- Performance: > 90
- First Contentful Paint: < 1s
- Time to Interactive: < 2s

---

## 🔍 Troubleshooting

### Backend no inicia:
```bash
# Ver logs del servicio
sudo journalctl -u taller-diego-backend -f

# O si usas uvicorn directamente:
tail -f /var/log/taller-diego-backend.log
```

### Nginx no recarga:
```bash
# Ver errores de configuración
sudo nginx -t

# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log
```

### Service Worker no se registra:
- Verificar que `service-worker.js` esté en la raíz del sitio
- Verificar en DevTools → Application → Service Workers
- El Service Worker solo funciona en HTTPS o localhost

### Caché no funciona:
```bash
# Limpiar caché del navegador completamente
# DevTools → Application → Clear storage → Clear site data

# Verificar en Console:
localStorage.clear()
# Luego recargar la página
```

---

## 📊 Resultados Esperados

| Métrica | Antes | Después |
|---------|-------|---------|
| CSS Load | 2s | < 200ms |
| Data Load (primera carga) | 3s | < 500ms |
| Data Load (con caché) | 3s | < 50ms |
| Total Load | 5s | < 1s |
| FCP | 2s | < 500ms |
| TTI | 5s | < 1.5s |

---

## 🎯 Próximos Pasos (Opcional)

Si aún necesitas más optimización:

1. **CDN**: Usar Cloudflare para servir assets estáticos
2. **Image Optimization**: Comprimir imágenes con WebP
3. **Code Splitting**: Dividir JavaScript en chunks más pequeños
4. **Database Indexing**: Agregar índices en Supabase
5. **HTTP/2**: Habilitar HTTP/2 en Nginx (si no está habilitado)

---

## 📝 Notas Importantes

- El caché de localStorage expira después de 5 minutos
- El caché del backend expira después de 5 minutos
- Los headers de Nginx cachean assets estáticos por 1 año
- El Service Worker cachea assets offline indefinidamente (hasta que se actualice)
- Al agregar/editar/eliminar productos, el caché se invalida automáticamente
