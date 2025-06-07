from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    ROLE_CHOICES = [
        ('administrator', 'Administrator'),
        ('secretariat', 'Sekretariat'),
        ('user', 'Użytkownik'),
    ]

    STATUS_CHOICES = [
        ('available', 'Dostępny'),
        ('busy', 'Zajęty'),
        ('offline', 'Niedostępny'),
    ]

    rola = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.username


class WorkSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def duration(self):
        from django.utils.timezone import now
        if self.logout_time:
            return self.logout_time - self.login_time
        return now() - self.login_time

    def __str__(self):
        return f"{self.user.username} | {self.login_time} - {self.logout_time or 'aktywny'}"

User = get_user_model()
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.sender} → {self.receiver} | {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.title} ({self.date})"