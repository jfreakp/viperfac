# 📧 Actualización: Email con URL Personalizable

## 🔧 Cambios Realizados

### 1. **Variable SITE_URL Configurada**
- ✅ Agregado `SITE_URL` en `.env` para controlar la URL base
- ✅ Importado en `settings.py` como variable configurable
- ✅ Modificado `auth/views.py` para usar `settings.SITE_URL` en lugar de `request.build_absolute_uri()`

### 2. **Template de Email Profesional**
- ✅ Creado `templates/auth/emails/password_reset.html`
- ✅ Diseño moderno con gradientes y tipografía profesional
- ✅ Responsive design para móviles y desktop
- ✅ Branding ViperFac con logo y colores corporativos

### 3. **Mejora en el Envío de Emails**
- ✅ Implementado `EmailMultiAlternatives` para HTML + texto plano
- ✅ Manejo de errores mejorado
- ✅ Enlace de desarrollo visible solo en modo DEBUG

## 🌐 Configuración de URL por Entorno

### **Desarrollo Local:**
```env
SITE_URL=http://127.0.0.1:8000
```

### **Producción:**
```env
# Heroku
SITE_URL=https://viperfac.herokuapp.com

# Dominio propio
SITE_URL=https://viperfac.com

# Vercel/Netlify
SITE_URL=https://viperfac.vercel.app
```

## 📱 Resultado Final

Cuando un usuario solicita recuperar su contraseña:

1. **Email HTML Profesional** con diseño moderno
2. **URL Correcta** basada en `SITE_URL` (no localhost)
3. **Botón Llamativo** para restablecer contraseña
4. **URL de Fallback** por si el botón no funciona
5. **Información de Seguridad** (24 horas de expiración)

## 🔄 Flujo de Trabajo

```
Usuario → Forgot Password → Email Enviado → Click Enlace → Reset Password
   ↓
Gmail SMTP → Template HTML → URL Personalizada → Formulario Seguro
```

## ⚡ Comandos para Usar

### **Cambiar a Producción:**
```bash
# Editar .env
SITE_URL=https://tu-dominio.com
```

### **Probar en Desarrollo:**
```bash
python manage.py runserver
# Ir a: http://127.0.0.1:8000/auth/forgot-password/
```

## 🎯 Próximos Pasos Sugeridos

1. **Deploy a Producción**: Configurar `SITE_URL` con tu dominio real
2. **Personalizar Branding**: Modificar colores y logo en el template
3. **Agregar Analytics**: Trackear clicks en emails (opcional)
4. **SSL Certificate**: Asegurar HTTPS para producción

¡Tu sistema ViperFac ahora envía emails profesionales con URLs correctas! 🚀