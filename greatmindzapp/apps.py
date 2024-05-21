from django.apps import AppConfig


class GreatmindzappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'greatmindzapp'

    def ready(self):
        import greatmindzapp.signals
