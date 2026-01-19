from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch
from bcp.models import Gestor

class ForcePasswordChangeMiddleware:
    """
    Middleware que fuerza a los usuarios a cambiar la clave si
    gestor.must_change_password = True.
    Permite logout sin bloqueo.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:

            # 🔹 Resolver URLs de manera segura
            try:
                cambiar_clave_url = reverse('cambiar_clave')
            except NoReverseMatch:
                cambiar_clave_url = '/cambiar-clave/'  # fallback

            try:
                logout_url = reverse('logout')
            except NoReverseMatch:
                logout_url = '/logout/'  # fallback

            # 🔹 Permitir logout sin bloquear
            if request.path.startswith(logout_url):
                return self.get_response(request)

            # 🔹 Revisar must_change_password
            try:
                gestor = Gestor.objects.get(user_gestor=request.user)
                if gestor.must_change_password:
                    # Si la request no es para cambiar clave, redirige
                    if not request.path.startswith(cambiar_clave_url):
                        return redirect(cambiar_clave_url)
            except Gestor.DoesNotExist:
                # Usuario no tiene Gestor asociado, no hacer nada
                pass

        # 🔹 Continuar con la request
        response = self.get_response(request)
        return response



