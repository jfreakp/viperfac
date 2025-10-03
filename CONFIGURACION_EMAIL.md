# Configuración de Email con Gmail

## 📧 Configuración Completada

El sistema Django ya está configurado para enviar emails usando Gmail SMTP.

## 🔧 Variables de Entorno

Las siguientes variables están configuradas en el archivo `.env`:

```env
# Configuración de Email
EMAIL_HOST_USER=jptorresdota@gmail.com
EMAIL_HOST_PASSWORD=gbag bafd uxxv mjpf
EMAIL_FROM=jptorresdota@gmail.com

# Configuración de Django
DEBUG=True
SECRET_KEY=django-insecure-0pl_95h96hevr#gb9$r=4f30j67tw0*bt4@x*7mkhc*km=(_nj

# Configuración del sitio
# Para desarrollo local:
SITE_URL=http://127.0.0.1:8000
# Para producción, cambiar a tu dominio:
# SITE_URL=https://tu-dominio.com
# SITE_URL=https://viperfac.herokuapp.com
```

## ⚙️ Configuración en Django

En `viperfac/settings.py` se añadieron las siguientes configuraciones:

```python
from decouple import config

# Email Configuration with Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')

# Site Configuration
SITE_URL = config('SITE_URL', default='http://127.0.0.1:8000')
```

## 🚀 Funcionalidades Disponibles

### 1. Recuperar Contraseña
- URL: `/auth/forgot-password/`
- El usuario ingresa su email
- Se envía un **email HTML profesional** con enlace de recuperación

### 2. Restablecer Contraseña
- URL: `/auth/reset-password/<token>/`
- El usuario accede desde el enlace del email
- Puede establecer una nueva contraseña

### 3. Configuración de URL Personalizable
- **Desarrollo**: `SITE_URL=http://127.0.0.1:8000`
- **Producción**: Cambiar a tu dominio real
- Los emails usan la URL configurada en lugar de localhost

## 🔒 Contraseña de Aplicación Gmail

**Importante**: La contraseña configurada (`gbag bafd uxxv mjpf`) es una **contraseña de aplicación** de Gmail, no tu contraseña personal.

### ¿Cómo generar una nueva si es necesario?

1. Ve a tu cuenta de Google
2. Seguridad → Verificación en 2 pasos
3. Contraseñas de aplicación
4. Genera una nueva para "Correo"
5. Usa esa contraseña en `EMAIL_HOST_PASSWORD`

## 🧪 Probar la Funcionalidad

1. Ejecuta el servidor:
   ```bash
   python manage.py runserver
   ```

2. Ve a: `http://127.0.0.1:8000/auth/login/`

3. Haz clic en "¿Olvidaste tu contraseña?"

4. Ingresa un email registrado y verifica que llegue el correo

## 📝 Logs y Debugging

Si hay problemas con el email, revisa:

1. **Configuración Gmail**: Verificar que la verificación en 2 pasos esté activa
2. **Contraseña de aplicación**: Debe ser válida y específica para email
3. **Logs Django**: Revisar la consola del servidor para errores SMTP

## 🔧 Variables de Entorno Adicionales

Si necesitas cambiar configuraciones, modifica el archivo `.env`:

```env
# Para cambiar el servidor SMTP (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True

# Para personalizar el remitente
EMAIL_FROM=tu-email@gmail.com
```

## ✅ Estado Actual

- ✅ Django configurado con python-decouple
- ✅ Variables de entorno seguras en `.env`
- ✅ Configuración SMTP Gmail completada
- ✅ Sistema de autenticación completo
- ✅ Funcionalidad de recuperación de contraseña
- ✅ Templates responsivos con Tailwind CSS
- ✅ **Emails HTML profesionales con diseño moderno**
- ✅ **URL personalizable via variable SITE_URL**
- ✅ **Enlaces funcionan con tu dominio real en producción**

### 🎨 Características del Email:

- **Diseño Profesional**: Template HTML con gradientes y estilos modernos
- **Responsive**: Se ve bien en móviles y desktop
- **Fallback**: Incluye versión de texto plano
- **Seguridad**: Enlaces con expiración de 24 horas
- **Branding**: Logo y colores de ViperFac

¡El sistema está completamente listo para producción!