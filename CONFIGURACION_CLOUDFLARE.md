# ☁️ Configuración de AdventureLog con Cloudflare

Esta guía te muestra cómo configurar AdventureLog con un subdominio de Cloudflare para acceso seguro desde internet.

## 🎯 Dos Métodos Disponibles

### Método 1: Cloudflare Tunnel (Recomendado - MÁS SEGURO)
- ✅ No necesitas abrir puertos en tu router
- ✅ SSL automático
- ✅ Protección DDoS de Cloudflare
- ✅ No expone tu IP pública

### Método 2: DNS + Port Forwarding (Tradicional)
- Necesitas abrir puertos en tu router
- SSL manual con certbot
- IP pública expuesta

---

## 🚀 Método 1: Cloudflare Tunnel (RECOMENDADO)

### Paso 1: Crear el Tunnel en Cloudflare

1. Ve a [Cloudflare Zero Trust](https://one.dash.cloudflare.com/)
2. En el menú lateral: **Access** → **Tunnels**
3. Click en **Create a tunnel**
4. Dale un nombre: `adventurelog-tunnel`
5. Click en **Save tunnel**

### Paso 2: Instalar cloudflared en TrueNAS

**Opción A: Usando Custom App en TrueNAS**

1. Ve a **Apps** → **Discover Apps** → **Custom App**
2. Nombre: `cloudflared-tunnel`
3. Container Image:
   - Repository: `cloudflare/cloudflared`
   - Tag: `latest`
4. Container Args:
   ```
   tunnel
   --no-autoupdate
   run
   --token
   TU_TOKEN_DE_CLOUDFLARE
   ```
   (El token lo obtienes en el paso anterior de Cloudflare)
5. Network: Bridge
6. Click **Save**

**Opción B: Usando Docker Compose (vía SSH)**

Crea un archivo `cloudflared-compose.yml`:

```yaml
version: '3.8'

services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared-tunnel
    restart: unless-stopped
    command: tunnel --no-autoupdate run --token TU_TOKEN_DE_CLOUDFLARE
    network_mode: host
```

Ejecuta:
```bash
docker-compose -f cloudflared-compose.yml up -d
```

### Paso 3: Configurar Public Hostnames

De vuelta en Cloudflare Tunnel:

1. En la sección **Public Hostname**, click **Add a public hostname**

**Para el Frontend:**
- Subdomain: `trekking` (o el nombre que quieras)
- Domain: `tudominio.com`
- Path: (dejar vacío)
- Type: `HTTP`
- URL: `adventurelog-frontend:3000`
  - Si usas docker-compose: `localhost:8015`

**Para el Backend (API):**
- Subdomain: `trekking-api` (o el nombre que quieras)
- Domain: `tudominio.com`
- Path: (dejar vacío)
- Type: `HTTP`
- URL: `adventurelog-backend:8000`
  - Si usas docker-compose: `localhost:8016`

Click **Save tunnel**

### Paso 4: Actualizar Variables de Entorno

Edita tu `.env`:

```bash
# Cambia esto:
PUBLIC_URL=https://trekking.tudominio.com

# Y esto:
CSRF_TRUSTED_ORIGINS=https://trekking.tudominio.com

# Asegúrate que el frontend sepa dónde está el backend
# (esto se maneja automáticamente, pero verifica que funcione)
```

### Paso 5: Reiniciar Contenedores

```bash
cd /mnt/yourpool/adventurelog
docker-compose -f docker-compose.prod.yml restart
```

### Paso 6: Verificar

1. Accede a: `https://trekking.tudominio.com`
2. Deberías ver AdventureLog con SSL funcionando
3. No necesitas port forwarding en tu router

---

## 🔧 Método 2: DNS + Port Forwarding (Tradicional)

### Paso 1: Configurar DNS en Cloudflare

1. Ve a tu dominio en Cloudflare
2. Click en **DNS** → **Records**
3. **Add record**:
   - Type: `A`
   - Name: `trekking` (o el subdominio que quieras)
   - IPv4 address: Tu IP pública
   - Proxy status: 🟠 **DNS only** (no proxy, inicialmente)
   - TTL: Auto
4. Click **Save**

### Paso 2: Port Forwarding en tu Router

1. Accede a tu router (usualmente `192.168.1.1` o `192.168.0.1`)
2. Busca la sección **Port Forwarding** o **NAT**
3. Crea estas reglas:

**Frontend:**
- External Port: `80` o `443`
- Internal IP: IP de tu TrueNAS
- Internal Port: `8015`
- Protocol: TCP

**Backend (opcional, solo si necesitas acceso directo al admin):**
- External Port: `8016`
- Internal IP: IP de tu TrueNAS
- Internal Port: `8016`
- Protocol: TCP

### Paso 3: Configurar SSL con Let's Encrypt

**Opción A: Usando Nginx Proxy Manager en TrueNAS**

1. Instala Nginx Proxy Manager como Custom App:
   - Image: `jc21/nginx-proxy-manager`
   - Port 80: `80`
   - Port 81: `81` (admin interface)
   - Port 443: `443`

2. Accede a `http://TU_IP_TRUENAS:81`
   - Email: `admin@example.com`
   - Password: `changeme`

3. Añade Proxy Host:
   - Domain Names: `trekking.tudominio.com`
   - Scheme: `http`
   - Forward Hostname: `adventurelog-frontend`
   - Forward Port: `3000`
   - SSL: Request new certificate (Let's Encrypt)

**Opción B: Usando Cloudflare Proxy (más fácil)**

1. En Cloudflare DNS, cambia el record de DNS only a **Proxied** (🟠 → 🟡)
2. Ve a **SSL/TLS** → **Overview**
3. Selecciona **Full** o **Full (strict)**
4. En **Edge Certificates**, activa:
   - ✅ Always Use HTTPS
   - ✅ Automatic HTTPS Rewrites

### Paso 4: Actualizar Variables de Entorno

```bash
# En .env
PUBLIC_URL=https://trekking.tudominio.com
CSRF_TRUSTED_ORIGINS=https://trekking.tudominio.com
```

### Paso 5: Reiniciar

```bash
docker-compose -f docker-compose.prod.yml restart
```

---

## 🔒 Seguridad Adicional con Cloudflare

### 1. Activar Firewall Rules (Opcional)

En Cloudflare:
1. Ve a **Security** → **WAF**
2. Crea reglas para proteger tu app:
   - Bloquear países específicos
   - Rate limiting
   - Challenge on suspicious activity

### 2. Activar Access (Opcional - Autenticación Extra)

Para agregar una capa extra de autenticación:

1. Ve a **Zero Trust** → **Access** → **Applications**
2. **Add an application**
3. Selecciona **Self-hosted**
4. Configura:
   - Application name: `AdventureLog`
   - Domain: `trekking.tudominio.com`
5. Añade políticas de acceso (email, Google login, etc.)

---

## 📝 Configuración Final Recomendada (.env)

```bash
# ==================================
# PRODUCCIÓN CON CLOUDFLARE
# ==================================

# Tu subdominio de Cloudflare
PUBLIC_URL=https://trekking.tudominio.com
CSRF_TRUSTED_ORIGINS=https://trekking.tudominio.com

# Puertos (solo para acceso interno, Cloudflare maneja los externos)
FRONTEND_PORT=8015
BACKEND_PORT=8016

# Base de Datos
POSTGRES_DB=adventurelog
POSTGRES_USER=adventurelog
POSTGRES_PASSWORD=tu_password_super_seguro_2024!

# Django (genera una clave única con: openssl rand -base64 32)
DJANGO_SECRET_KEY=tu_clave_secreta_generada_aleatoriamente_aqui
DJANGO_ADMIN_USERNAME=admin
DJANGO_ADMIN_PASSWORD=tu_password_admin_muy_seguro
DJANGO_ADMIN_EMAIL=tu_email@tudominio.com

# Seguridad
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=trekking.tudominio.com,localhost,127.0.0.1

# Email (opcional - para recuperación de contraseñas)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password_de_gmail
DEFAULT_FROM_EMAIL=AdventureLog <noreply@tudominio.com>
```

---

## ✅ Checklist de Configuración

### Con Cloudflare Tunnel:
- [ ] Tunnel creado en Cloudflare
- [ ] cloudflared instalado en TrueNAS
- [ ] Public hostnames configurados
- [ ] `.env` actualizado con `https://trekking.tudominio.com`
- [ ] Contenedores reiniciados
- [ ] Puedes acceder a `https://trekking.tudominio.com`
- [ ] SSL funciona (candado verde en el navegador)

### Con DNS + Port Forwarding:
- [ ] DNS A record creado en Cloudflare
- [ ] Port forwarding configurado en router
- [ ] Nginx Proxy Manager o Cloudflare Proxy configurado
- [ ] SSL activo (Let's Encrypt o Cloudflare)
- [ ] `.env` actualizado
- [ ] Contenedores reiniciados
- [ ] HTTPS funciona

---

## 🆘 Troubleshooting

### Error: "Too Many Redirects"

**Causa**: Configuración SSL/TLS incorrecta

**Solución**:
1. En Cloudflare: **SSL/TLS** → **Overview**
2. Cambia a **Full** (no Flexible, no Full Strict)

### Error: "CSRF verification failed"

**Causa**: `CSRF_TRUSTED_ORIGINS` incorrecto

**Solución**:
```bash
# En .env, usa exactamente la URL con https://
CSRF_TRUSTED_ORIGINS=https://trekking.tudominio.com
```

Reinicia:
```bash
docker-compose -f docker-compose.prod.yml restart server
```

### Error: "502 Bad Gateway"

**Causa**: El contenedor frontend no puede conectar al backend

**Solución**:
```bash
# Verifica que ambos estén corriendo
docker ps

# Ve los logs
docker logs adventurelog-frontend
docker logs adventurelog-backend

# Reinicia
docker-compose -f docker-compose.prod.yml restart
```

---

## 🎉 Acceso Final

Después de configurar Cloudflare, tu app estará disponible en:

**Con Tunnel:**
- 🌐 Frontend: `https://trekking.tudominio.com`
- 🔧 Backend Admin: `https://trekking-api.tudominio.com/admin`

**Con DNS + Port Forwarding:**
- 🌐 Frontend: `https://trekking.tudominio.com`
- 🔧 Backend Admin: `https://trekking.tudominio.com:8016/admin` (si abriste el puerto)

¡Todo con SSL gratis de Cloudflare! 🔒

---

## 💡 Recomendación

**Usa Cloudflare Tunnel** si puedes. Es más seguro, más fácil de configurar (no necesitas tocar el router), y Cloudflare maneja todo el SSL y protección DDoS automáticamente.
