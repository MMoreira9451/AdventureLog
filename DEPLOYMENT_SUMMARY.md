# Resumen de Configuración de Deploy

## 📦 Archivos Modificados/Creados

### 1. **docker-compose.yml** (Modificado)
- Agregado Nginx Proxy Manager como servicio
- Todos los servicios ahora en red compartida `adventurelog-network`
- Puertos internos expuestos solo dentro de la red
- Nginx Proxy Manager maneja puertos 80, 443, 81

### 2. **docker-compose.prod.yml** (Modificado)
- Igual estructura que docker-compose.yml pero usa imágenes de GHCR
- Variables de entorno configuradas desde `.env.production`
- Preparado para CI/CD automático

### 3. **.env** (Creado)
Configuración para desarrollo local:
```env
ORIGIN=https://trekings.ashyweb.win
PUBLIC_URL=https://trekings.ashyweb.win
CSRF_TRUSTED_ORIGINS=https://trekings.ashyweb.win
```

### 4. **.env.production.example** (Actualizado)
- Template para producción
- Simplificado a un solo dominio
- Instrucciones claras

### 5. **.github/workflows/deploy.yml** (Creado)
Workflow de GitHub Actions que:
- Se activa cuando los builds terminan
- Conecta al servidor por SSH
- Hace pull de nuevas imágenes
- Reinicia contenedores
- Verifica que el deploy fue exitoso

### 6. **NGINX_SETUP.md** (Creado)
Guía paso a paso para configurar Nginx Proxy Manager

### 7. **CICD_SETUP.md** (Actualizado)
Guía completa del flujo CI/CD con SSH deploy

## 🔄 Flujo de Deploy Completo

```
┌─────────────────────────────────────────────────────────────┐
│                    DESARROLLO LOCAL                          │
└─────────────────────────────────────────────────────────────┘
                            │
                    git push origin main
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS                            │
├─────────────────────────────────────────────────────────────┤
│  1. Build Backend Docker Image                              │
│     └─> Push to ghcr.io/usuario/backend:latest              │
│                                                              │
│  2. Build Frontend Docker Image                             │
│     └─> Push to ghcr.io/usuario/frontend:latest             │
│                                                              │
│  3. Deploy to Production Server                             │
│     ├─> SSH al servidor                                     │
│     ├─> docker compose pull                                 │
│     ├─> docker compose up -d --force-recreate               │
│     └─> Verificar contenedores corriendo                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                SERVIDOR PRODUCCIÓN                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────┐                     │
│  │   Nginx Proxy Manager :80/443      │                     │
│  └───────────┬────────────────────────┘                     │
│              │                                               │
│     ┌────────┴─────────┐                                    │
│     ▼                  ▼                                     │
│  Frontend :3000    Backend :80                              │
│     │                  │                                     │
│     │                  ▼                                     │
│     │            PostgreSQL :5432                            │
│     │                                                        │
│     └─────────────────────┘                                 │
│                                                              │
│  URL: https://trekings.ashyweb.win                          │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Configuración en el Servidor

### Estructura de archivos esperada:
```
/root/adventurelog/  (o la ruta que definas)
├── docker-compose.prod.yml
├── .env.production
└── (otros archivos del repo)
```

### `.env.production` debe contener:
```env
GITHUB_USERNAME=ghcr.io/TU_USUARIO
PUBLIC_URL=https://trekings.ashyweb.win
CSRF_TRUSTED_ORIGINS=https://trekings.ashyweb.win
POSTGRES_DB=adventurelog
POSTGRES_USER=adventurelog
POSTGRES_PASSWORD=password_seguro
DJANGO_SECRET_KEY=clave_secreta_larga
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_PASSWORD=password_admin
DJANGO_ADMIN_EMAIL=tu@email.com
```

## 🔐 GitHub Secrets Requeridos

Configurar en: **GitHub repo → Settings → Secrets → Actions**

| Secret | Valor |
|--------|-------|
| `DEPLOY_HOST` | `192.168.4.111` |
| `DEPLOY_USER` | `root` (o tu usuario SSH) |
| `DEPLOY_SSH_KEY` | Clave privada SSH completa |
| `DEPLOY_PATH` | `/root/adventurelog` |
| `DEPLOY_PORT` | `22` (opcional) |

## 🚀 Primera Instalación

### 1. En el servidor (192.168.4.111):

```bash
# Clonar repo
git clone https://github.com/TU_USUARIO/AdventureLog.git /root/adventurelog
cd /root/adventurelog

# Crear .env.production
cp .env.production.example .env.production
nano .env.production  # Editar con tus valores

# Login a GHCR (si las imágenes son privadas)
echo "TU_GITHUB_TOKEN" | docker login ghcr.io -u TU_USUARIO --password-stdin

# Iniciar servicios
docker compose -f docker-compose.prod.yml up -d

# Esperar 60 segundos
sleep 60

# Verificar estado
docker compose -f docker-compose.prod.yml ps
```

### 2. Configurar Nginx Proxy Manager:

Accede a: `http://192.168.4.111:81`

**Login inicial:**
- Email: `admin@example.com`
- Password: `changeme123`

**Configurar Proxy Host:**
- Domain: `trekings.ashyweb.win`
- Forward to: `adventurelog-frontend:3000`
- SSL: Solicitar certificado Let's Encrypt
- Advanced: Ver `NGINX_SETUP.md` para configuración completa

### 3. Configurar GitHub Actions:

```bash
# En tu máquina local
ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/github_deploy
ssh-copy-id -i ~/.ssh/github_deploy.pub root@192.168.4.111

# Copiar clave privada y agregarla como secret en GitHub
cat ~/.ssh/github_deploy
```

Agregar secrets en GitHub (ver sección "GitHub Secrets Requeridos")

## ✅ Verificación

### 1. Verificar que los contenedores están corriendo:
```bash
docker compose -f docker-compose.prod.yml ps
```

Deberías ver:
- ✅ adventurelog-frontend (Up)
- ✅ adventurelog-backend (Up)
- ✅ adventurelog-db (Up)
- ✅ nginx-proxy-manager (Up)

### 2. Verificar que Nginx está configurado:
Accede a `https://trekings.ashyweb.win` → Deberías ver la app

### 3. Verificar CI/CD:
```bash
# Hacer un cambio pequeño
echo "# Test" >> README.md
git add README.md
git commit -m "Test CI/CD"
git push origin main
```

Ve a GitHub → Actions → Deberías ver los workflows ejecutándose

## 🎉 Resultado Final

Después de esta configuración:

1. ✅ **Un solo dominio:** `https://trekings.ashyweb.win`
2. ✅ **Sin error 500:** CSRF configurado correctamente
3. ✅ **Deploy automático:** Push a main = Deploy en 5 minutos
4. ✅ **SSL automático:** Let's Encrypt via Nginx Proxy Manager
5. ✅ **Logs centralizados:** En GitHub Actions
6. ✅ **Base de datos persistente:** Volúmenes Docker preservados

## 📚 Documentación Adicional

- **NGINX_SETUP.md**: Configuración detallada de Nginx Proxy Manager
- **CICD_SETUP.md**: Guía completa del flujo CI/CD
- **.env.production.example**: Template de configuración

## 🆘 Ayuda

Si algo falla:
1. Revisa logs: `docker compose -f docker-compose.prod.yml logs -f`
2. Verifica secrets de GitHub
3. Confirma que `.env.production` está configurado
4. Consulta la sección Troubleshooting en `CICD_SETUP.md`
