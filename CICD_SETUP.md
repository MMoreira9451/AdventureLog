# Configuración CI/CD para AdventureLog

## 📋 Flujo de CI/CD

El flujo automático funciona así:

1. **Push a `main`** → Activa los workflows de build
2. **Build Backend** → Construye y sube imagen a GHCR
3. **Build Frontend** → Construye y sube imagen a GHCR
4. **Deploy** → Se activa automáticamente cuando los builds terminan exitosamente
5. **Servidor** → Descarga las nuevas imágenes y reinicia los contenedores

## 🔐 Secrets de GitHub Requeridos

Ve a: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Agrega los siguientes secrets:

| Secret Name | Descripción | Ejemplo |
|-------------|-------------|---------|
| `DEPLOY_HOST` | IP o dominio del servidor | `192.168.4.111` |
| `DEPLOY_USER` | Usuario SSH del servidor | `root` o `admin` |
| `DEPLOY_SSH_KEY` | Clave privada SSH (contenido completo) | Ver sección "Generar SSH Key" |
| `DEPLOY_PATH` | Ruta donde está el proyecto en el servidor | `/root/adventurelog` |
| `DEPLOY_PORT` | Puerto SSH (opcional, default: 22) | `22` |

## 🔑 Generar SSH Key para Deploy

### En tu máquina local (Mac/Linux):

```bash
# Generar nueva clave SSH específica para deploy
ssh-keygen -t ed25519 -C "github-deploy-adventurelog" -f ~/.ssh/github_deploy

# Copiar clave pública al servidor
ssh-copy-id -i ~/.ssh/github_deploy.pub usuario@192.168.4.111

# Copiar clave PRIVADA para agregarla como secret en GitHub
cat ~/.ssh/github_deploy
```

### Agregar clave privada a GitHub:

1. Copia **TODO** el contenido de `cat ~/.ssh/github_deploy` (incluye `-----BEGIN OPENSSH PRIVATE KEY-----` y `-----END OPENSSH PRIVATE KEY-----`)
2. Ve a GitHub → Settings → Secrets → New secret
3. Name: `DEPLOY_SSH_KEY`
4. Value: Pega todo el contenido de la clave privada

## 📦 Preparar el Servidor

### 1. Clonar el repositorio en el servidor

```bash
ssh usuario@192.168.4.111

# Clonar tu fork
git clone https://github.com/TU_USUARIO/AdventureLog.git
cd AdventureLog

# Copiar y configurar .env.production
cp .env.production.example .env.production
nano .env.production
```

### 2. Configurar `.env.production` en el servidor

Edita con tus valores reales:

```env
GITHUB_USERNAME=ghcr.io/TU_USUARIO_GITHUB
PUBLIC_URL=https://trekings.ashyweb.win
CSRF_TRUSTED_ORIGINS=https://trekings.ashyweb.win

POSTGRES_DB=adventurelog
POSTGRES_USER=adventurelog
POSTGRES_PASSWORD=TU_PASSWORD_SEGURO_123

DJANGO_SECRET_KEY=clave_secreta_larga_y_aleatoria_generada
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_PASSWORD=TU_PASSWORD_ADMIN_SEGURO
DJANGO_ADMIN_EMAIL=tu_email@example.com
```

### 3. Iniciar por primera vez

```bash
# Login en GitHub Container Registry (si tu repo es privado)
echo "TU_GITHUB_TOKEN" | docker login ghcr.io -u TU_USUARIO --password-stdin

# Iniciar servicios
docker compose -f docker-compose.prod.yml up -d

# Ver logs
docker compose -f docker-compose.prod.yml logs -f
```

## 🚀 Uso del CI/CD

### Deploy Automático

Simplemente haz push a `main`:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

El workflow se ejecutará automáticamente:
1. Build Backend (si hubo cambios en `backend/`)
2. Build Frontend (si hubo cambios en `frontend/`)
3. Deploy automático cuando los builds terminen

### Deploy Manual

Si necesitas hacer un deploy sin cambios en el código:

1. Ve a **Actions** en GitHub
2. Selecciona **"Deploy to Production Server"**
3. Click en **"Run workflow"** → **"Run workflow"**

## 📊 Monitoreo

### Ver estado del workflow en GitHub

Ve a la pestaña **Actions** en tu repositorio.

### Ver logs en el servidor

```bash
ssh usuario@192.168.4.111
cd /ruta/del/proyecto
docker compose -f docker-compose.prod.yml logs -f web     # Frontend
docker compose -f docker-compose.prod.yml logs -f server  # Backend
docker compose -f docker-compose.prod.yml ps              # Estado
```

## 🔧 Troubleshooting

### Error: "Permission denied (publickey)"

La clave SSH no está configurada correctamente:

```bash
# En el servidor, verifica que la clave pública esté en authorized_keys
cat ~/.ssh/authorized_keys | grep "github-deploy-adventurelog"

# Si no está, vuelve a copiarla
ssh-copy-id -i ~/.ssh/github_deploy.pub usuario@192.168.4.111
```

### Error: "Cannot pull image"

Login en GHCR no está configurado o token expiró:

```bash
# En el servidor
echo "TU_GITHUB_TOKEN" | docker login ghcr.io -u TU_USUARIO --password-stdin
```

### Deploy falla pero los builds son exitosos

Verifica que:
1. El archivo `docker-compose.prod.yml` existe en el servidor
2. El archivo `.env.production` está configurado correctamente
3. Los secrets `DEPLOY_PATH` apunta a la ruta correcta

## 📝 Notas Importantes

- Los volúmenes de Docker (base de datos, media files) se mantienen entre deploys
- Solo se recrean los contenedores `web` y `server`, NO la base de datos
- Nginx Proxy Manager mantiene su configuración entre deploys
- Las imágenes antiguas se limpian automáticamente después del deploy

## 🎯 Flujo Completo de Ejemplo

```bash
# 1. Hacer cambios en el código
vim frontend/src/routes/+page.svelte

# 2. Commit y push
git add .
git commit -m "Update homepage design"
git push origin main

# 3. GitHub Actions automáticamente:
#    - Construye nueva imagen frontend
#    - Sube imagen a ghcr.io
#    - Conecta al servidor por SSH
#    - Descarga nueva imagen
#    - Reinicia contenedor frontend
#    - Verifica que esté corriendo

# 4. ✅ Cambios en producción en ~5 minutos
```
