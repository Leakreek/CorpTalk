from django.apps import AppConfig
from django.utils.timezone import now

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        User.objects.all().update(status='offline')

        # Opcjonalnie zamknij trwające sesje
        from .models import WorkSession
        WorkSession.objects.filter(logout_time__isnull=True).update(logout_time=now())
