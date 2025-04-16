from django.apps import AppConfig


class EventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventos'

    def ready(self):
        import eventos.tasks
        import eventos.tasks_warning
        import eventos.tasks_error