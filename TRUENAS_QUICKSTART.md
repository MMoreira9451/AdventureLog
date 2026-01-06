# TrueNAS Scale - Instalación Rápida

## 🎯 Resumen: 4 Custom Apps a crear

```
1. PostgreSQL      → Base de datos
2. Backend         → Django API
3. Frontend        → SvelteKit UI
4. Nginx Proxy     → Reverse Proxy + SSL
```

---

## 📋 Valores de Configuración

### 🔐 Cambia estos valores antes de usarlos:

```env
# Base de datos
POSTGRES_PASSWORD=CAMBIA_ESTE_PASSWORD_123
DJANGO_SECRET_KEY=genera-una-clave-secreta-larga-y-aleatoria-aqui
DJANGO_ADMIN_PASSWORD=CAMBIA_ESTE_PASSWORD

# Dominio
PUBLIC_URL=https://trekings.ashyweb.win
CSRF_TRUSTED_ORIGINS=https://trekings.ashyweb.win

# GitHub (si usas tus propias imágenes)
GITHUB_USERNAME=TU_USUARIO_GITHUB
```

---

## 📦 APP 1: PostgreSQL

**Image:** `postgis/postgis:16-3.5`

**Variables de entorno:**
```
POSTGRES_DB=adventurelog
POSTGRES_USER=adventurelog
POSTGRES_PASSWORD=TU_PASSWORD_AQUI
```

**Puerto:** `5432` → `5432`

**Volumen:**
```
/mnt/tu-pool/adventurelog/postgres-data → /var/lib/postgresql/data
```

---

## 📦 APP 2: Backend

**Image:** `ghcr.io/seanmorley15/adventurelog-backend:latest`
(O tu imagen: `ghcr.io/TU_USUARIO/adventurelog-trekking-backend:latest`)

**Variables de entorno:**
```
PGHOST=adventurelog-db.ix-adventurelog-db.svc.cluster.local
POSTGRES_DB=adventurelog
POSTGRES_USER=adventurelog
POSTGRES_PASSWORD=TU_PASSWORD_AQUI
SECRET_KEY=TU_CLAVE_SECRETA_AQUI
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_PASSWORD=TU_PASSWORD_ADMIN
DJANGO_ADMIN_EMAIL=tu@email.com
PUBLIC_URL=https://trekings.ashyweb.win
CSRF_TRUSTED_ORIGINS=https://trekings.ashyweb.win
DEBUG=False
FRONTEND_URL=https://trekings.ashyweb.win
```

**Puerto:** `80` → `80` (Cluster IP)

**Volumen:**
```
/mnt/tu-pool/adventurelog/media → /code/media
```

---

## 📦 APP 3: Frontend

**Image:** `ghcr.io/seanmorley15/adventurelog-frontend:latest`
(O tu imagen: `ghcr.io/TU_USUARIO/adventurelog-trekking-frontend:latest`)

**Variables de entorno:**
```
PUBLIC_SERVER_URL=http://adventurelog-backend.ix-adventurelog-backend.svc.cluster.local:80
ORIGIN=https://trekings.ashyweb.win
BODY_SIZE_LIMIT=Infinity
```

**Puerto:** `3000` → `3000` (Cluster IP)

**Sin volúmenes**

---

## 📦 APP 4: Nginx Proxy Manager

**Image:** `jc21/nginx-proxy-manager:latest`

**Puertos (Node Port o LoadBalancer):**
```
80  → 30080 (HTTP)
443 → 30443 (HTTPS)
81  → 30081 (Admin UI)
```

**Volúmenes:**
```
/mnt/tu-pool/adventurelog/npm-data → /data
/mnt/tu-pool/adventurelog/npm-letsencrypt → /etc/letsencrypt
```

---

## 🔧 Configurar Nginx Proxy Manager

### 1. Acceder:
```
http://IP_TRUENAS:30081
```

**Login:**
- Email: `admin@example.com`
- Password: `changeme123`

### 2. Crear Proxy Host:

**Details:**
- Domain: `trekings.ashyweb.win`
- Scheme: `http`
- Forward to: `adventurelog-frontend.ix-adventurelog-frontend.svc.cluster.local`
- Port: `3000`

**SSL:**
- Request new SSL Certificate (Let's Encrypt)
- ✅ Force SSL

**Advanced:**
```nginx
location /api/ {
    proxy_pass http://adventurelog-backend.ix-adventurelog-backend.svc.cluster.local:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /media/ {
    proxy_pass http://adventurelog-backend.ix-adventurelog-backend.svc.cluster.local:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /admin/ {
    proxy_pass http://adventurelog-backend.ix-adventurelog-backend.svc.cluster.local:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## 🌐 Configurar Router

**Port Forwarding:**
```
Puerto 80  → TrueNAS_IP:30080
Puerto 443 → TrueNAS_IP:30443
```

**DNS:**
```
trekings.ashyweb.win → TU_IP_PUBLICA
```

---

## ✅ Verificación

1. Todas las apps en estado **Running** en TrueNAS
2. Acceder a `https://trekings.ashyweb.win`
3. Login con `admin` / tu password
4. Crear una aventura de prueba

---

## 📁 Crear Directorios (antes de instalar)

Por SSH en TrueNAS:
```bash
mkdir -p /mnt/tu-pool/adventurelog/postgres-data
mkdir -p /mnt/tu-pool/adventurelog/media
mkdir -p /mnt/tu-pool/adventurelog/npm-data
mkdir -p /mnt/tu-pool/adventurelog/npm-letsencrypt
```

---

## 🆘 Problemas Comunes

### Error: "Cannot connect to database"
- Verifica que PostgreSQL esté **Running**
- Verifica el nombre del servicio en `PGHOST`

### Error 502 en Nginx
- Verifica que frontend/backend estén **Running**
- Revisa los nombres de servicio en Nginx config

### Error 500 en la app
- Verifica que `PUBLIC_URL` y `CSRF_TRUSTED_ORIGINS` sean iguales
- Deben ser HTTPS si usas dominio

---

## 📚 Documentación Completa

Para instrucciones detalladas paso a paso, ver **TRUENAS_SETUP.md**
