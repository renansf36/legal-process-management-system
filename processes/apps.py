from django.apps import AppConfig


class ProcessesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "processes"
    verbose_name = "Gestao Juridica"

    def ready(self):
        import processes.signals  # noqa: F401
