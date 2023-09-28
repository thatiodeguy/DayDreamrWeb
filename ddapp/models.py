from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime, timedelta

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)

class Roadmap(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __init__(self, title: str, description: str, owner: CustomUser):
        self.title = title
        self.description = description
        self.owner = owner

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)

    def __init__(self, title: str, description: str, roadmap: Roadmap):
        self.title = title
        self.description = description
        self.roadmap = roadmap

class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=datetime.now() + timedelta(hours=1))
    
    def is_expired(self):
        return datetime.now() > self.expires_at