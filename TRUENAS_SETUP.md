# Instalación de AdventureLog en TrueNAS Scale

## 📋 Resumen

TrueNAS Scale usa **Kubernetes** (no Docker Compose), así que crearemos cada servicio como "Custom App" a través de la interfaz web.

## 🎯 Servicios a crear

1. **PostgreSQL con PostGIS** (Base de datos)
2. **AdventureLog Backend** (Django API)
3. **AdventureLog Frontend** (SvelteKit)
4. **Nginx Proxy Manager** (Reverse Proxy)

---

## 📦 PASO 1: Crear Base de Datos PostgreSQL

### 1.1 Ir a Apps
- TrueNAS Scale Web UI → **Apps** → **Discover Apps**
- Click en **Custom App** (arriba a la derecha)

### 1.2 Configuración Básica

**Application Name:**
```
adventurelog-db
```

**Image Repository:**
```
postgis/postgis
```

**Image Tag:**
```
16-3.5
```

**Image Pull Policy:**
```
If not present
```

### 1.3 Container Environment Variables

Click en **Add** para cada variable:

| Variable | Valor |
|----------|-------|
| `POSTGRES_DB` | `adventurelog` |
| `POSTGRES_USER` | `adventurelog` |
| `POSTGRES_PASSWORD` | `TU_PASSWORD_SEGURO_123` |

### 1.4 Networking

**Enable Host Network:** ❌ NO

**Add External Interfaces** → **Add**:
- **Type:** `LoadBalancer Service`
- **Port:** `5432`
- **Target Port:** `5432`
- **Protocol:** `TCP`

### 1.5 Storage

**Host Path Volumes** → **Add**:

**Volume 1:**
- **Type:** `Host Path`
- **Host Path:** `/mnt/tu-pool/adventurelog/postgres-data`
- **Mount Path:** `/var/lib/postgresql/data`
- **Read Only:** ❌ NO

### 1.6 Security

- **Run as User ID:** `999` (postgres user)
- **Run as Group ID:** `999`

Click **Save** y espera a que el contenedor esté en estado **Running**.

---

## 📦 PASO 2: Crear Backend (Django)

### 2.1 Custom App

**Apps** → **Discover Apps** → **Custom App**

### 2.2 Configuración Básica

**Application Name:**
```
adventurelog-backend
```

**Image Repository:**
```
ghcr.io/TU_USUARIO_GITHUB/adventurelog-trekking-backend
```
(O usa la imagen oficial: `ghcr.io/seanmorley15/adventurelog-backend`)

**Image Tag:**
```
latest
```

**Image Pull Policy:**
```
Always
```

### 2.3 Container Environment Variables

Click en **Add** para cada una:

| Variable | Valor |
|----------|-------|
| `PGHOST` | `adventurelog-db.ix-adventurelog-db.svc.cluster.local` |
| `POSTGRES_DB` | `adventurelog` |
| `POSTGRES_USER` | `adventurelog` |
| `POSTGRES_PASSWORD` | `TU_PASSWORD_SEGURO_123` |
| `SECRET_KEY` | `clave-secreta-larga-y-aleatoria-generada` |
| `DJANGO_ADMIN_USERNAME` | `admin` |
| `DJANGO_ADMIN_PASSWORD` | `TU_PASSWORD_ADMIN` |
| `DJANGO_ADMIN_EMAIL` | `tu@email.com` |
| `PUBLIC_URL` | `https://trekings.ashyweb.win` |
| `CSRF_TRUSTED_ORIGINS` | `https://trekings.ashyweb.win` |
| `DEBUG` | `False` |
| `FRONTEND_URL` | `https://trekings.ashyweb.win` |

**IMPORTANTE:** El `PGHOST` debe ser el nombre del servicio de Kubernetes. El formato es:
```
nombre-app.ix-nombre-app.svc.cluster.local
```

### 2.4 Networking

**Enable Host Network:** ❌ NO

**Add External Interfaces** → **Add**:
- **Type:** `Cluster IP`
- **Port:** `80`
- **Target Port:** `80`
- **Protocol:** `TCP`

### 2.5 Storage

**Host Path Volumes** → **Add**:

**Volume 1 - Media Files:**
- **Type:** `Host Path`
- **Host Path:** `/mnt/tu-pool/adventurelog/media`
- **Mount Path:** `/code/media`
- **Read Only:** ❌ NO

### 2.6 Security

- **Privileged Mode:** ❌ NO
- **Run as User ID:** `0` (root, required para Django)
- **Run as Group ID:** `0`

Click **Save**.

---

## 📦 PASO 3: Crear Frontend (SvelteKit)

### 3.1 Custom App

**Apps** → **Discover Apps** → **Custom App**

### 3.2 Configuración Básica

**Application Name:**
```
adventurelog-frontend
```

**Image Repository:**
```
ghcr.io/TU_USUARIO_GITHUB/adventurelog-trekking-frontend
```
(O imagen oficial: `ghcr.io/seanmorley15/adventurelog-frontend`)

**Image Tag:**
```
latest
```

**Image Pull Policy:**
```
Always
```

### 3.3 Container Environment Variables

| Variable | Valor |
|----------|-------|
| `PUBLIC_SERVER_URL` | `http://adventurelog-backend.ix-adventurelog-backend.svc.cluster.local:80` |
| `ORIGIN` | `https://trekings.ashyweb.win` |
| `BODY_SIZE_LIMIT` | `Infinity` |

### 3.4 Networking

**Enable Host Network:** ❌ NO

**Add External Interfaces** → **Add**:
- **Type:** `Cluster IP`
- **Port:** `3000`
- **Target Port:** `3000`
- **Protocol:** `TCP`

### 3.5 Storage

No necesita volúmenes persistentes.

### 3.6 Security

- **Run as User ID:** `0`
- **Run as Group ID:** `0`

Click **Save**.

---

## 📦 PASO 4: Crear Nginx Proxy Manager

### 4.1 Custom App

**Apps** → **Discover Apps** → **Custom App**

### 4.2 Configuración Básica

**Application Name:**
```
nginx-proxy-manager
```

**Image Repository:**
```
jc21/nginx-proxy-manager
```

**Image Tag:**
```
latest
```

### 4.3 Networking

**Enable Host Network:** ❌ NO

**Add External Interfaces** → **Add 3 puertos**:

**Puerto 1 - HTTP:**
- **Type:** `Node Port` (o LoadBalancer si TrueNAS lo permite)
- **Port:** `80`
- **Node Port:** `30080` (puedes usar otro)
- **Target Port:** `80`
- **Protocol:** `TCP`

**Puerto 2 - HTTPS:**
- **Type:** `Node Port`
- **Port:** `443`
- **Node Port:** `30443`
- **Target Port:** `443`
- **Protocol:** `TCP`

**Puerto 3 - Admin UI:**
- **Type:** `Node Port`
- **Port:** `81`
- **Node Port:** `30081`
- **Target Port:** `81`
- **Protocol:** `TCP`

### 4.4 Storage

**Host Path Volumes** → **Add 2 volúmenes**:

**Volume 1 - Data:**
- **Host Path:** `/mnt/tu-pool/adventurelog/npm-data`
- **Mount Path:** `/data`
- **Read Only:** ❌ NO

**Volume 2 - Let's Encrypt:**
- **Host Path:** `/mnt/tu-pool/adventurelog/npm-letsencrypt`
- **Mount Path:** `/etc/letsencrypt`
- **Read Only:** ❌ NO

### 4.5 Security

- **Run as User ID:** `0`
- **Run as Group ID:** `0`

Click **Save**.

---

## ⚙️ PASO 5: Configurar Nginx Proxy Manager

### 5.1 Acceder a la UI

Abre en tu navegador:
```
http://IP_DE_TRUENAS:30081
```

**Login por defecto:**
- Email: `admin@example.com`
- Password: `changeme123`

**CAMBIA la contraseña** en el primer login.

### 5.2 Agregar Proxy Host

**Proxy Hosts** → **Add Proxy Host**

#### Tab "Details":
- **Domain Names:** `trekings.ashyweb.win`
- **Scheme:** `http`
- **Forward Hostname/IP:** `adventurelog-frontend.ix-adventurelog-frontend.svc.cluster.local`
- **Forward Port:** `3000`
- ✅ **Cache Assets**
- ✅ **Block Common Exploits**
- ✅ **Websockets Support**

#### Tab "SSL":
- **SSL Certificate:** Request a new SSL Certificate
- **Email:** Tu email
- ✅ **Agree to Terms**
- ✅ **Force SSL**
- ✅ **HTTP/2 Support**
- ✅ **HSTS Enabled**

#### Tab "Advanced":

```nginx
# Proxy backend API requests
location /api/ {
    proxy_pass http://adventurelog-backend.ix-adventurelog-backend.svc.cluster.local:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Proxy media files
location /media/ {
    proxy_pass http://adventurelog-backend.ix-adventurelog-backend.svc.cluster.local:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Proxy admin panel
location /admin/ {
    proxy_pass http://adventurelog-backend.ix-adventurelog-backend.svc.cluster.local:80;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Click **Save**.

---

## 🌐 PASO 6: Configurar Router/Firewall

### 6.1 Port Forwarding en tu Router

Redirige estos puertos externos a TrueNAS:

| Puerto Externo | Puerto TrueNAS | Servicio |
|----------------|----------------|----------|
| `80` | `30080` | HTTP |
| `443` | `30443` | HTTPS |

### 6.2 DNS

En tu proveedor de dominio (donde compraste `ashyweb.win`):

Agrega un registro A:
```
trekings.ashyweb.win → TU_IP_PUBLICA
```

---

## ✅ PASO 7: Verificación

### 7.1 Verificar Apps en TrueNAS

**Apps** → Todas las apps deben estar en estado **Running**:
- ✅ adventurelog-db
- ✅ adventurelog-backend
- ✅ adventurelog-frontend
- ✅ nginx-proxy-manager

### 7.2 Verificar Logs

Si alguna app falla, revisa los logs:
- Click en la app → **Logs**

### 7.3 Probar la Aplicación

Accede a: `https://trekings.ashyweb.win`

Deberías poder:
- ✅ Ver la página de login
- ✅ Login con `admin` / tu password
- ✅ Crear aventuras sin error 500

---

## 🔄 PASO 8: Configurar Auto-Actualización (Opcional)

### Opción A: Watchtower (Recomendado)

**Apps** → **Discover Apps** → **Custom App**

**Application Name:** `watchtower`

**Image Repository:** `containrrr/watchtower`

**Image Tag:** `latest`

**Container Args:**
```
--interval
3600
--cleanup
```

**Container Entrypoint:**
```
/watchtower
```

**Storage - Host Path Volumes:**
- **Host Path:** `/var/run/k3s/containerd/containerd.sock`
- **Mount Path:** `/var/run/docker.sock`
- **Read Only:** ✅ YES

**IMPORTANTE:** En TrueNAS Scale, el socket de Kubernetes está en:
```
/var/run/k3s/containerd/containerd.sock
```

### Opción B: Actualización Manual

Cada vez que hagas cambios:

1. **Apps** → Click en la app
2. **Edit**
3. No cambies nada, solo click **Save**
4. TrueNAS descargará la última versión de la imagen

---

## 🔐 Acceso a Imágenes Privadas en GitHub

Si tus imágenes en GHCR son privadas:

### 8.1 Crear Personal Access Token en GitHub

1. GitHub → **Settings** → **Developer settings**
2. **Personal access tokens** → **Tokens (classic)**
3. **Generate new token (classic)**
4. Permisos: ✅ `read:packages`
5. Copia el token

### 8.2 Configurar en TrueNAS

Para cada app (frontend/backend):

1. **Edit** la app
2. Sección **Image Pull Policy**
3. **Add** credentials:
   - **Registry:** `ghcr.io`
   - **Username:** `TU_USUARIO_GITHUB`
   - **Password:** `TU_GITHUB_TOKEN`

---

## 📊 Estructura de Volúmenes en TrueNAS

Crea estos directorios antes de instalar:

```
/mnt/tu-pool/adventurelog/
├── postgres-data/       # Base de datos PostgreSQL
├── media/              # Archivos subidos (imágenes, GPX)
├── npm-data/           # Configuración de Nginx Proxy Manager
└── npm-letsencrypt/    # Certificados SSL
```

Puedes crearlos desde:
- **Storage** → **Pools** → Click en el pool → **Add Dataset**
- O por SSH: `mkdir -p /mnt/tu-pool/adventurelog/{postgres-data,media,npm-data,npm-letsencrypt}`

---

## 🆘 Troubleshooting

### Error: "Cannot connect to database"

El backend no puede conectar a PostgreSQL. Verifica:

1. **Apps** → **adventurelog-db** → **Logs**
2. Confirma que PostgreSQL está corriendo
3. Verifica que `PGHOST` en backend sea:
   ```
   adventurelog-db.ix-adventurelog-db.svc.cluster.local
   ```

Para encontrar el nombre correcto del servicio:
- **Apps** → **adventurelog-db** → **Workloads** → Copia el nombre del servicio

### Error: "502 Bad Gateway" en Nginx

El frontend/backend no están respondiendo. Verifica:

1. Que las apps estén en estado **Running**
2. Los logs de frontend/backend
3. Que los nombres de servicio en Nginx Proxy Manager sean correctos

### Error: "Image pull failed"

Las imágenes son privadas y no configuraste credenciales. Ver sección "Acceso a Imágenes Privadas".

### Error 500 en la aplicación

CSRF mal configurado. Verifica que:
- `PUBLIC_URL` = `https://trekings.ashyweb.win`
- `CSRF_TRUSTED_ORIGINS` = `https://trekings.ashyweb.win`
- Son exactamente iguales (no mezcles http/https)

---

## 🎉 Ventajas de TrueNAS Scale

✅ **UI amigable:** Todo desde la interfaz web
✅ **Snapshots:** Backups automáticos de volúmenes
✅ **Actualizaciones fáciles:** Un click para actualizar apps
✅ **Aislamiento:** Cada app en su propio namespace de Kubernetes
✅ **Monitoreo:** Logs y métricas integradas

---

## 💡 Próximos Pasos

Después de tener todo funcionando:

1. **Configurar backups automáticos** de los volúmenes
2. **Configurar snapshots** en TrueNAS para la base de datos
3. **Agregar monitoreo** con Prometheus (TrueNAS lo incluye)
4. **Configurar notificaciones** en Nginx Proxy Manager para certificados

¡Tu AdventureLog está ahora corriendo en TrueNAS Scale! 🚀🏔️
