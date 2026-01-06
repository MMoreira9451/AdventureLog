# 🏔️ Guía de Instalación de AdventureLog en TrueNAS SCALE

Esta guía te ayudará a deployear AdventureLog en tu servidor TrueNAS SCALE.

## 📋 Pre-requisitos

- TrueNAS SCALE instalado y funcionando
- Acceso a la interfaz web de TrueNAS
- Conocimientos básicos de Docker y TrueNAS

## 🎯 Método 1: Usando Custom App (Recomendado)

### Paso 1: Crear Datasets para Datos Persistentes

1. Ve a **Storage** → **Your Pool** → **Create Dataset**
2. Crea los siguientes datasets:
   - `adventurelog-db` (para PostgreSQL)
   - `adventurelog-media` (para archivos de usuario)

### Paso 2: Instalar Custom App

1. Ve a **Apps** en el menú lateral
2. Click en **Discover Apps**
3. Click en **Custom App** (botón arriba a la derecha)

### Paso 3: Configurar la Base de Datos (PostgreSQL)

**Nombre de la App:** `adventurelog-db`

**Container Images:**
- Image repository: `postgis/postgis`
- Image Tag: `16-3.5`

**Container Environment Variables:**
```
POSTGRES_DB=adventurelog
POSTGRES_USER=adventurelog
POSTGRES_PASSWORD=TU_PASSWORD_SEGURO_123
```

**Storage:**
- Host Path: `/mnt/yourpool/adventurelog-db`
- Mount Path: `/var/lib/postgresql/data`

**Network:**
- Deja las opciones por defecto (bridge network)

Click en **Save** y espera a que la app esté "Running"

### Paso 4: Configurar el Backend (Django)

**Nombre de la App:** `adventurelog-backend`

**Container Images:**
- Image repository: `ghcr.io/seanmorley15/adventurelog`
- Image Tag: `latest`

**Container Environment Variables:**
```
PGHOST=adventurelog-db.ix-adventurelog-db.svc.cluster.local
PGDATABASE=adventurelog
PGUSER=adventurelog
PGPASSWORD=TU_PASSWORD_SEGURO_123
DJANGO_SECRET_KEY=GENERA_UNA_CLAVE_LARGA_Y_ALEATORIA
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_PASSWORD=TU_PASSWORD_ADMIN
DJANGO_ADMIN_EMAIL=tu_email@example.com
PUBLIC_URL=http://TU_IP_TRUENAS:8015
CSRF_TRUSTED_ORIGINS=http://TU_IP_TRUENAS:8015
DJANGO_DEBUG=False
```

**Port Forwarding:**
- Container Port: `8000`
- Node Port: `8016`
- Protocol: TCP

**Storage:**
- Host Path: `/mnt/yourpool/adventurelog-media`
- Mount Path: `/code/media`

Click en **Save**

### Paso 5: Configurar el Frontend (SvelteKit)

**Nombre de la App:** `adventurelog-frontend`

**Container Images:**
- Image repository: `ghcr.io/seanmorley15/adventurelog-frontend`
- Image Tag: `latest`

**Container Environment Variables:**
```
ORIGIN=http://TU_IP_TRUENAS:8015
BODY_SIZE_LIMIT=Infinity
```

**Port Forwarding:**
- Container Port: `3000`
- Node Port: `8015`
- Protocol: TCP

Click en **Save**

### Paso 6: Verificar Instalación

1. Ve a **Apps** y verifica que las 3 apps estén en estado "Running"
2. Accede a: `http://TU_IP_TRUENAS:8015`
3. Inicia sesión con las credenciales de admin que configuraste

---

## 🐳 Método 2: Usando Docker Compose (Avanzado)

### Paso 1: Habilitar SSH en TrueNAS

1. Ve a **System Settings** → **Services**
2. Habilita y inicia el servicio **SSH**

### Paso 2: Subir Archivos a TrueNAS

1. Conecta por SSH: `ssh admin@TU_IP_TRUENAS`
2. Crea un directorio:
   ```bash
   mkdir -p /mnt/yourpool/adventurelog
   cd /mnt/yourpool/adventurelog
   ```

3. Sube los archivos `docker-compose.prod.yml` y `.env.production`:
   - Usando SCP desde tu PC:
   ```bash
   scp docker-compose.prod.yml admin@TU_IP_TRUENAS:/mnt/yourpool/adventurelog/
   scp .env.production admin@TU_IP_TRUENAS:/mnt/yourpool/adventurelog/.env
   ```

### Paso 3: Editar Variables de Entorno

Conecta por SSH y edita el archivo .env:

```bash
cd /mnt/yourpool/adventurelog
nano .env
```

**IMPORTANTE:** Cambia estas variables:
- `PUBLIC_URL`: Tu IP de TrueNAS (ej: `http://192.168.1.100:8015`)
- `POSTGRES_PASSWORD`: Una contraseña segura
- `DJANGO_SECRET_KEY`: Una clave secreta larga y aleatoria
- `DJANGO_ADMIN_PASSWORD`: Contraseña para el admin
- `DJANGO_ADMIN_EMAIL`: Tu email

### Paso 4: Generar Django Secret Key

```bash
# Genera una clave secreta aleatoria
openssl rand -base64 32
```

Copia el resultado y úsalo como `DJANGO_SECRET_KEY`

### Paso 5: Iniciar los Contenedores

```bash
cd /mnt/yourpool/adventurelog
docker-compose -f docker-compose.prod.yml up -d
```

### Paso 6: Verificar Estado

```bash
docker-compose -f docker-compose.prod.yml ps
```

Deberías ver 3 contenedores en estado "Up":
- adventurelog-frontend
- adventurelog-backend
- adventurelog-db

### Paso 7: Ver Logs (si hay problemas)

```bash
# Ver logs del backend
docker-compose -f docker-compose.prod.yml logs server

# Ver logs del frontend
docker-compose -f docker-compose.prod.yml logs web

# Ver logs de la base de datos
docker-compose -f docker-compose.prod.yml logs db
```

---

## 🔧 Configuración Post-Instalación

### 1. Cambiar el Idioma a Español

1. Accede a `http://TU_IP_TRUENAS:8015`
2. Inicia sesión con el admin
3. Ve a **Settings** (⚙️ en la navbar)
4. Selecciona **Language** → **Español**

### 2. Configurar Backup Automático

TrueNAS puede hacer snapshots automáticos de los datasets:

1. Ve a **Data Protection** → **Periodic Snapshot Tasks**
2. Crea snapshot para:
   - `adventurelog-db` (cada día, retención 7 días)
   - `adventurelog-media` (cada día, retención 30 días)

### 3. Configurar Acceso Externo (Opcional)

Si quieres acceder desde fuera de tu red:

**Opción A: Port Forwarding en tu Router**
1. Abre los puertos 8015 y 8016 en tu router
2. Apúntalos a la IP de tu TrueNAS

**Opción B: Reverse Proxy con Nginx Proxy Manager**
1. Instala Nginx Proxy Manager en TrueNAS
2. Configura un proxy para AdventureLog
3. Usa un dominio con SSL

---

## 🔒 Seguridad Recomendada

### 1. Cambia las Contraseñas por Defecto

```bash
# Accede al contenedor del backend
docker exec -it adventurelog-backend bash

# Crea un nuevo superuser
python manage.py createsuperuser

# Elimina el usuario admin por defecto desde el panel de admin
```

### 2. Configura HTTPS

Si expones la app a internet, DEBES usar HTTPS:
- Usa Nginx Proxy Manager con Let's Encrypt
- O usa Cloudflare Tunnel

### 3. Backups

Configura backups regulares:
- Snapshots de TrueNAS para los datasets
- Exporta backups desde la app (Settings → Backup)

---

## 📊 Monitoreo

### Ver Uso de Recursos

```bash
# CPU y Memoria
docker stats

# Espacio en disco
df -h /mnt/yourpool/adventurelog-*
```

### Logs en Tiempo Real

```bash
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 🔄 Actualizaciones

### Actualizar a Nueva Versión

```bash
cd /mnt/yourpool/adventurelog

# Detener contenedores
docker-compose -f docker-compose.prod.yml down

# Hacer backup
docker-compose -f docker-compose.prod.yml exec db pg_dump -U adventurelog adventurelog > backup_$(date +%Y%m%d).sql

# Actualizar imágenes
docker-compose -f docker-compose.prod.yml pull

# Iniciar con nuevas imágenes
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 🆘 Solución de Problemas

### Problema: "502 Bad Gateway" en el frontend

**Solución:**
```bash
# Verifica que el backend esté funcionando
docker-compose -f docker-compose.prod.yml logs server

# Reinicia el frontend
docker-compose -f docker-compose.prod.yml restart web
```

### Problema: "Database connection error"

**Solución:**
```bash
# Verifica que la DB esté corriendo
docker-compose -f docker-compose.prod.yml ps db

# Verifica los logs de la DB
docker-compose -f docker-compose.prod.yml logs db

# Verifica las credenciales en .env
cat .env | grep POSTGRES
```

### Problema: "CSRF verification failed"

**Solución:**
Edita `.env` y asegúrate que:
```
PUBLIC_URL=http://TU_IP_REAL:8015
CSRF_TRUSTED_ORIGINS=http://TU_IP_REAL:8015
```

Luego reinicia:
```bash
docker-compose -f docker-compose.prod.yml restart server
```

---

## 📝 Comandos Útiles

```bash
# Ver todos los contenedores
docker ps -a

# Ver logs de un contenedor específico
docker logs adventurelog-backend

# Acceder a la shell del backend
docker exec -it adventurelog-backend bash

# Acceder a PostgreSQL
docker exec -it adventurelog-db psql -U adventurelog -d adventurelog

# Backup manual de la base de datos
docker exec adventurelog-db pg_dump -U adventurelog adventurelog > backup.sql

# Restaurar backup
docker exec -i adventurelog-db psql -U adventurelog -d adventurelog < backup.sql

# Detener todo
docker-compose -f docker-compose.prod.yml down

# Iniciar todo
docker-compose -f docker-compose.prod.yml up -d

# Reconstruir y reiniciar
docker-compose -f docker-compose.prod.yml up -d --build --force-recreate
```

---

## ✅ Checklist de Deployment

- [ ] Datasets creados en TrueNAS
- [ ] Variables de entorno configuradas en `.env`
- [ ] `DJANGO_SECRET_KEY` generada y única
- [ ] Contraseñas cambiadas por defecto
- [ ] `PUBLIC_URL` y `CSRF_TRUSTED_ORIGINS` configurados correctamente
- [ ] Contenedores en estado "Running"
- [ ] Puedes acceder a `http://TU_IP:8015`
- [ ] Login con credenciales de admin funciona
- [ ] Idioma cambiado a Español
- [ ] Snapshots automáticos configurados
- [ ] Backup manual realizado

---

## 🎉 ¡Listo!

Tu instancia de AdventureLog debería estar funcionando en:
- **Frontend**: `http://TU_IP_TRUENAS:8015`
- **Backend Admin**: `http://TU_IP_TRUENAS:8016/admin`

¡Empieza a registrar tus rutas de trekking! 🏔️
