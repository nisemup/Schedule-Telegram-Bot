from django.apps import AppConfig


class ScheduleAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        from .signals import set_start_end_time
