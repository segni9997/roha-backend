from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    verbose_name = '1. Studio Profile & Page Builder'

    def ready(self):
        try:
            import pillow_heif
            pillow_heif.register_heif_opener()
        except Exception:
            pass
