from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
import uuid

@csrf_protect
def login_view(request):
    """Vista para el login de usuarios"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'¡Bienvenido {user.first_name or user.username}!')
                    next_url = request.GET.get('next', 'dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Tu cuenta está desactivada. Contacta al administrador.')
            else:
                messages.error(request, 'Credenciales inválidas. Por favor, intenta de nuevo.')
        else:
            messages.error(request, 'Por favor, completa todos los campos.')
    
    return render(request, 'auth/login.html')

@csrf_protect
def register_view(request):
    """Vista para el registro de nuevos usuarios"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validaciones
        if not all([username, email, first_name, last_name, password, confirm_password]):
            messages.error(request, 'Por favor, completa todos los campos.')
        elif password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado.')
        else:
            # Crear usuario
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                messages.success(request, '¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.')
                return redirect('login')
            except Exception as e:
                messages.error(request, 'Error al crear la cuenta. Por favor, intenta de nuevo.')
    
    return render(request, 'auth/register.html')

@csrf_protect
def forgot_password_view(request):
    """Vista para solicitar recuperación de contraseña"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if email:
            try:
                user = User.objects.get(email=email, is_active=True)
                
                # Generar token y URL de reseteo
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Crear el enlace de reseteo usando SITE_URL desde settings
                reset_url = f"{settings.SITE_URL}/auth/reset-password/{uid}/{token}/"
                
                # Preparar el email
                subject = 'Recuperación de Contraseña - ViperFac'
                message = f"""
Hola {user.first_name or user.username},

Has solicitado restablecer tu contraseña en ViperFac.

Haz clic en el siguiente enlace para crear una nueva contraseña:
{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este email.

Saludos,
Equipo ViperFac
                """
                
                # Preparar el email con template HTML
                try:
                    # Contexto para el template
                    email_context = {
                        'user_name': user.first_name or user.username,
                        'reset_url': reset_url,
                        'site_name': 'ViperFac',
                    }
                    
                    # Renderizar template HTML
                    html_message = render_to_string('auth/emails/password_reset.html', email_context)
                    
                    # Mensaje de texto plano como fallback
                    plain_message = f"""
Hola {user.first_name or user.username},

Has solicitado restablecer tu contraseña en ViperFac.

Enlace de recuperación: {reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, puedes ignorar este email.

Saludos,
Equipo ViperFac
                    """
                    
                    # Enviar el email con HTML y texto plano
                    from django.core.mail import EmailMultiAlternatives
                    
                    email_msg = EmailMultiAlternatives(
                        subject=subject,
                        body=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[email],
                    )
                    email_msg.attach_alternative(html_message, "text/html")
                    email_msg.send()
                    
                    messages.success(request, 
                        f'Se ha enviado un enlace de recuperación a {email}. '
                        f'Por favor, revisa tu bandeja de entrada.')
                    
                    # Mostrar el enlace solo en modo DEBUG para desarrollo
                    if settings.DEBUG:
                        messages.info(request, f'Enlace de desarrollo: {reset_url}')
                        
                except Exception as e:
                    messages.error(request, f'Error al enviar el email: {str(e)}')
                
            except User.DoesNotExist:
                # No revelar si el email existe o no por seguridad
                messages.success(request, 
                    'Si el email existe en nuestro sistema, recibirás un enlace de recuperación.')
        else:
            messages.error(request, 'Por favor, ingresa tu email.')
    
    return render(request, 'auth/forgot_password.html')

@csrf_protect
def reset_password_view(request, uidb64, token):
    """Vista para resetear la contraseña con token"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password and confirm_password:
                if new_password == confirm_password:
                    if len(new_password) >= 8:
                        user.set_password(new_password)
                        user.save()
                        messages.success(request, 'Tu contraseña ha sido actualizada exitosamente.')
                        return redirect('login')
                    else:
                        messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                else:
                    messages.error(request, 'Las contraseñas no coinciden.')
            else:
                messages.error(request, 'Por favor, completa todos los campos.')
        
        return render(request, 'auth/reset_password.html', {'validlink': True})
    else:
        messages.error(request, 'El enlace de recuperación es inválido o ha expirado.')
        return redirect('forgot_password')

def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('login')

@login_required
def dashboard_view(request):
    """Vista del dashboard principal (requiere autenticación)"""
    return render(request, 'auth/dashboard.html', {
        'user': request.user
    })

@login_required
def profile_view(request):
    """Vista del perfil de usuario"""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        
        # Cambiar contraseña si se proporciona
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        
        if current_password and new_password:
            if user.check_password(current_password):
                if len(new_password) >= 8:
                    user.set_password(new_password)
                    messages.success(request, 'Perfil y contraseña actualizados exitosamente.')
                else:
                    messages.error(request, 'La nueva contraseña debe tener al menos 8 caracteres.')
                    return render(request, 'auth/profile.html', {'user': user})
            else:
                messages.error(request, 'La contraseña actual es incorrecta.')
                return render(request, 'auth/profile.html', {'user': user})
        else:
            messages.success(request, 'Perfil actualizado exitosamente.')
        
        user.save()
        return redirect('profile')
    
    return render(request, 'auth/profile.html', {'user': request.user})
