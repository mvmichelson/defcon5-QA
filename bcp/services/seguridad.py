# Funciones de Seguridad de  negocio Sistema Defcon5

import random
import string
from django.core.mail import send_mail
from django.conf import settings

def generar_clave_temporal(longitud=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

def resetear_clave_gestor(gestor):
    if not gestor.user_gestor:
        raise ValueError("El gestor no tiene usuario asociado")

    nueva_clave = generar_clave_temporal()

    user = gestor.user_gestor
    user.set_password(nueva_clave)
    user.save()

    gestor.must_change_password = True
    gestor.save()

    send_mail(
        subject='Reseteo de clave de acceso',
        message=(
            f'Su nueva clave temporal es: {nueva_clave}\n\n'
            'Al ingresar por primera vez, el sistema le solicitará cambiarla.'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
