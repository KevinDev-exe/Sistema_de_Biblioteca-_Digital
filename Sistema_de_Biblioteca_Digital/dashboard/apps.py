from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dashboard"
    verbose_name = "Dashboard"

    def ready(self):
        from django.contrib.auth.models import User
        User.es_bibliotecario = property(lambda self: hasattr(self, 'perfil') and self.perfil.rol == 'ADMIN')

