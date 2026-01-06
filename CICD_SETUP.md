# 🔄 CI/CD Automático: GitHub → Imágenes Docker → TrueNAS

Esta guía configura un sistema automático donde cualquier cambio en GitHub se refleja automáticamente en TrueNAS.

## 🎯 Flujo Automático

```
Haces cambio en código (Git)
    ↓
GitHub Actions detecta cambio
    ↓
Construye imagen Docker automáticamente
    ↓
Sube imagen a GitHub Container Registry
    ↓
Watchtower en TrueNAS detecta nueva imagen
    ↓
TrueNAS actualiza la app automáticamente
```

---

## 📋 PASO 1: Preparar GitHub Repository

### 1.1 Crear tu propio fork/repo

Si aún usas el repo original de AdventureLog, necesitas crear tu propio repo:

**Opción A: Fork**
1. Ve a https://github.com/seanmorley15/AdventureLog
2. Click en **Fork** (arriba a la derecha)
3. Crea el fork en tu cuenta

**Opción B: Nuevo Repo con tus cambios**
1. Crea un nuevo repo en GitHub (ej: `adventurelog-trekking`)
2. Sube tu código modificado:

```bash
cd C:\Users\mmore\OneDrive\Escritorio\condominio\AdventureLog

# Inicializa git si no lo has hecho
git init
git add .
git commit -m "Transformación a app de trekking en español"

# Conecta con tu repo de GitHub
git remote add origin https://github.com/TU_USUARIO/adventurelog-trekking.git
git branch -M main
git push -u origin main
```

### 1.2 Habilitar GitHub Actions

1. Ve a tu repo en GitHub
2. Click en **Settings** → **Actions** → **General**
3. En "Workflow permissions":
   - ✅ Marca "Read and write permissions"
   - ✅ Marca "Allow GitHub Actions to create and approve pull requests"
4. Click **Save**

### 1.3 Habilitar GitHub Container Registry

1. Ve a tu perfil de GitHub → **Settings**
2. **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. **Generate new token (classic)**
4. Permisos necesarios:
   - ✅ `write:packages`
   - ✅ `read:packages`
   - ✅ `delete:packages`
5. Copia el token y guárdalo (lo necesitarás después)

---

## 📋 PASO 2: Configurar GitHub Actions

Los archivos ya están creados en `.github/workflows/`:
- `build-frontend.yml`
- `build-backend.yml`

### 2.1 Subir los workflows a GitHub

```bash
cd C:\Users\mmore\OneDrive\Escritorio\condominio\AdventureLog

git add .github/workflows/
git commit -m "Add GitHub Actions workflows for Docker builds"
git push
```

### 2.2 Verificar que funcionan

1. Ve a tu repo en GitHub
2. Click en **Actions** (tab arriba)
3. Deberías ver 2 workflows corriendo:
   - "Build Frontend Docker Image"
   - "Build Backend Docker Image"
4. Espera ~5-10 minutos a que terminen

### 2.3 Ver las imágenes creadas

1. Ve a tu repo en GitHub
2. Click en tu nombre de usuario (arriba a la derecha) → **Your profile**
3. Click en **Packages** (tab)
4. Deberías ver:
   - `adventurelog-trekking/frontend`
   - `adventurelog-trekking/backend`

Las URLs serán algo como:
```
ghcr.io/TU_USUARIO/adventurelog-trekking/frontend:latest
ghcr.io/TU_USUARIO/adventurelog-trekking/backend:latest
```

---

## 📋 PASO 3: Configurar TrueNAS con tus imágenes

Ahora actualiza las Custom Apps en TrueNAS para usar TUS imágenes.

### 3.1 Actualizar Frontend App

1. En TrueNAS: **Apps** → **adventurelog-frontend** → **Edit**
2. Cambia **Image Repository**:
   ```
   ghcr.io/TU_USUARIO/adventurelog-trekking/frontend
   ```
3. **Image Tag**: `latest`
4. Click **Save**

### 3.2 Actualizar Backend App

1. En TrueNAS: **Apps** → **adventurelog-backend** → **Edit**
2. Cambia **Image Repository**:
   ```
   ghcr.io/TU_USUARIO/adventurelog-trekking/backend
   ```
3. **Image Tag**: `latest`
4. Click **Save**

TrueNAS descargará tus imágenes personalizadas y reiniciará las apps.

---

## 📋 PASO 4: Configurar Auto-Actualización con Watchtower

Watchtower es un contenedor que monitorea actualizaciones de imágenes y actualiza automáticamente.

### 4.1 Instalar Watchtower en TrueNAS

1. **Apps** → **Discover Apps** → **Custom App**

**Application Name:**
```
watchtower
```

**Image Repository:**
```
containrrr/watchtower
```

**Image Tag:**
```
latest
```

**Container Args:**
```
--interval
3600
--cleanup
```
(Esto revisa cada hora = 3600 segundos)

**Container Entrypoint:**
```
/watchtower
```

**Storage - Host Path Volumes:**
- Host Path: `/var/run/docker.sock`
- Mount Path: `/var/run/docker.sock`
- Read Only: ✅ Sí

**Networking:**
- No necesita puertos

Click **Save**

### 4.2 ¿Qué hace Watchtower?

- Revisa cada hora si hay nuevas versiones de las imágenes
- Si detecta una actualización:
  1. Descarga la nueva imagen
  2. Detiene el contenedor viejo
  3. Inicia el nuevo contenedor
  4. Elimina la imagen vieja

**Todo automático, sin downtime.**

---

## 📋 PASO 5: Hacer un Cambio y Verlo en Producción

### 5.1 Hacer un cambio en el código

Por ejemplo, cambiar un texto en el dashboard:

```bash
# Edita frontend/src/routes/dashboard/+page.svelte
# Cambia algo visual

git add .
git commit -m "Actualizar texto del dashboard"
git push
```

### 5.2 Ver el build automático

1. Ve a GitHub → **Actions**
2. Verás que se inició "Build Frontend Docker Image"
3. Espera ~5 minutos a que termine

### 5.3 Watchtower detecta y actualiza

- En la próxima hora, Watchtower detectará la nueva imagen
- Actualizará automáticamente en TrueNAS
- Refresh tu navegador en `https://trekking.tudominio.com`
- ¡Verás los cambios!

### 5.4 Ver logs de Watchtower

En TrueNAS:
- **Apps** → **watchtower** → **Logs**
- Verás mensajes como:
  ```
  Found new image for adventurelog-frontend
  Updating container...
  Successfully updated
  ```

---

## ⚡ Actualización Manual (Sin Esperar)

Si quieres ver los cambios inmediatamente sin esperar a Watchtower:

### Opción 1: Desde TrueNAS UI

1. **Apps** → **adventurelog-frontend** → **Edit**
2. No cambies nada, solo click **Save**
3. TrueNAS descarga la última imagen automáticamente

### Opción 2: Forzar Watchtower

1. **Apps** → **watchtower** → **Stop**
2. **Apps** → **watchtower** → **Start**
3. Watchtower revisa inmediatamente

---

## 🎛️ Configuración Avanzada de Watchtower

Para revisar cada 5 minutos en lugar de cada hora:

1. **Apps** → **watchtower** → **Edit**
2. **Container Args**:
   ```
   --interval
   300
   --cleanup
   ```
3. Click **Save**

Para solo monitorear ciertas apps:

**Container Args:**
```
--interval
3600
--cleanup
adventurelog-frontend
adventurelog-backend
```

Para recibir notificaciones (ej: email, Slack):

**Container Environment Variables:**
```
WATCHTOWER_NOTIFICATIONS=email
WATCHTOWER_NOTIFICATION_EMAIL_FROM=watchtower@tudominio.com
WATCHTOWER_NOTIFICATION_EMAIL_TO=tu@email.com
WATCHTOWER_NOTIFICATION_EMAIL_SERVER=smtp.gmail.com
WATCHTOWER_NOTIFICATION_EMAIL_SERVER_PORT=587
WATCHTOWER_NOTIFICATION_EMAIL_SERVER_USER=tu_email@gmail.com
WATCHTOWER_NOTIFICATION_EMAIL_SERVER_PASSWORD=tu_app_password
```

---

## 🔒 Imágenes Privadas (Opcional)

Si quieres que tus imágenes sean privadas:

### En GitHub:

1. Ve a tu paquete en GitHub
2. **Package settings** → **Change visibility**
3. Selecciona **Private**

### En TrueNAS (para acceder a imágenes privadas):

Necesitas configurar credenciales:

1. **Apps** → **adventurelog-frontend** → **Edit**
2. Sección **Advanced Settings** → **Image Pull Policy**
3. Añade credenciales de GitHub:
   - Registry: `ghcr.io`
   - Username: Tu usuario de GitHub
   - Password: Tu Personal Access Token

---

## 📊 Monitoreo del CI/CD

### Ver builds en GitHub

- GitHub → **Actions**
- Click en cualquier workflow
- Ve los logs completos del build

### Ver actualizaciones en TrueNAS

- **Apps** → **watchtower** → **Logs**
- Verás cuándo se actualizó cada contenedor

### Ver versión actual de la imagen

```bash
# SSH a TrueNAS (opcional)
docker inspect adventurelog-frontend | grep Image
```

---

## ✅ Resumen del Sistema Completo

**Desarrollo:**
```
1. Editas código en tu PC
2. git add, commit, push
3. GitHub Actions construye imagen
4. Imagen sube a ghcr.io automáticamente
```

**Producción:**
```
1. Watchtower revisa cada hora
2. Detecta nueva imagen
3. Actualiza contenedor en TrueNAS
4. Tus usuarios ven los cambios
```

**Todo automático, cero downtime, cero configuración manual.**

---

## 🎉 Ventajas de este Sistema

✅ **Push-to-Deploy**: Haces `git push` y en ~1 hora está en producción
✅ **Rollback fácil**: Si algo falla, Watchtower puede volver a la versión anterior
✅ **Cero downtime**: Watchtower hace rolling updates
✅ **Gratis**: GitHub Actions + ghcr.io son totalmente gratis
✅ **Logs completos**: Ves todo el proceso en GitHub Actions
✅ **Versionado**: Cada imagen tiene su SHA de git

---

## 🆘 Troubleshooting

### "Workflow failed" en GitHub Actions

- Ve a **Actions** → Click en el workflow fallido
- Lee el log para ver el error
- Usualmente es un error de sintaxis en Dockerfile

### Watchtower no actualiza

- Verifica logs: **Apps** → **watchtower** → **Logs**
- Asegúrate que `/var/run/docker.sock` está montado correctamente
- Verifica que la imagen tenga tag `latest`

### "Image pull failed" en TrueNAS

- La imagen es privada y necesitas credenciales
- O el nombre de la imagen está mal escrito

---

## 💡 Próximos Pasos

Ahora que tienes CI/CD configurado, puedes:

1. **Agregar tests automáticos** en GitHub Actions
2. **Crear ambientes de staging** (otra app en TrueNAS con tag `dev`)
3. **Notificaciones** cuando haya actualizaciones
4. **Backups automáticos** antes de cada actualización

¡Tu app de trekking ahora se actualiza sola! 🚀🏔️
