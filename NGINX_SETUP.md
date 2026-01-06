# Configuración de AdventureLog con Nginx Proxy Manager

## 📋 Resumen de cambios

Todo ahora está en **un solo docker-compose** con una red compartida (`adventurelog-network`).

## 🚀 Pasos de instalación

### 1. Copia los archivos al servidor

Copia estos archivos a tu servidor (192.168.4.111):
- `docker-compose.prod.yml`
- `.env.production.example` (y renómbralo a `.env.production`)

### 2. Configura las variables de entorno

```bash
# En el servidor
cd /ruta/del/proyecto
cp .env.production.example .env.production
nano .env.production
```

Edita con tus valores:
- `GITHUB_USERNAME`: Tu usuario de GitHub Container Registry
- `PUBLIC_URL`: Tu dominio (ej: https://trekings.ashyweb.win)
- `CSRF_TRUSTED_ORIGINS`: El mismo dominio
- Contraseñas seguras para PostgreSQL y Django

### 3. Inicia los contenedores

```bash
docker compose -f docker-compose.prod.yml down  # Si tienes contenedores anteriores
docker compose -f docker-compose.prod.yml up -d
```

**Espera 60 segundos** para que todos los servicios inicien.

### 3. Accede a Nginx Proxy Manager

Abre en tu navegador: `http://192.168.4.111:81`

**Credenciales por defecto:**
- Email: `admin@example.com`
- Password: `changeme123`

**IMPORTANTE:** Cambia la contraseña en el primer login.

### 4. Configura el Proxy Host para AdventureLog

En Nginx Proxy Manager, ve a **"Proxy Hosts"** → **"Add Proxy Host"**

#### Configuración:

**Tab "Details":**
- **Domain Names:** `trekings.ashyweb.win`
- **Scheme:** `http`
- **Forward Hostname/IP:** `adventurelog-frontend`
- **Forward Port:** `3000`
- ✅ **Cache Assets**
- ✅ **Block Common Exploits**
- ✅ **Websockets Support**

**Tab "SSL":**
- **SSL Certificate:** Request a new SSL Certificate (Let's Encrypt)
- ✅ **Force SSL**
- ✅ **HTTP/2 Support**
- ✅ **HSTS Enabled**

**Tab "Advanced":**
Agrega este código para manejar las rutas del backend:

```nginx
# Proxy backend API requests
location /api/ {
    proxy_pass http://adventurelog-backend:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Proxy media files
location /media/ {
    proxy_pass http://adventurelog-backend:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Proxy admin panel
location /admin/ {
    proxy_pass http://adventurelog-backend:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 5. Guarda y prueba

Guarda la configuración y accede a: **https://trekings.ashyweb.win**

## ✅ Verificación

Deberías poder:
- ✅ Acceder al frontend en `https://trekings.ashyweb.win`
- ✅ Login con `admin/admin`
- ✅ Ver imágenes correctamente
- ✅ Crear nuevas aventuras sin error 500

## 🔧 Troubleshooting

### Ver logs:
```bash
docker compose -f docker-compose.prod.yml logs -f web       # Frontend
docker compose -f docker-compose.prod.yml logs -f server    # Backend
docker compose -f docker-compose.prod.yml logs -f nginx-proxy-manager
```

### Reiniciar servicios:
```bash
docker compose -f docker-compose.prod.yml restart
```

### Error 500 persiste:
Verifica que `CSRF_TRUSTED_ORIGINS` en `.env.production` tenga exactamente: `https://trekings.ashyweb.win`

## 📝 Notas importantes

- **Ya NO necesitas** el dominio `trekings_back.ashyweb.win`
- **Un solo dominio** maneja todo (frontend + backend)
- Los puertos 80, 443 están ahora manejados por Nginx Proxy Manager
- El puerto 81 es para la admin UI de Nginx Proxy Manager (puedes cerrarlo en el firewall después de configurar)
