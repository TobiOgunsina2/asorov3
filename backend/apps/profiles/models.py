from django.db import models
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from apps.curriculum.models import Lesson

# Create your models here.

# Handles social media capabilities & public info. 
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    # Unique user display name
    display_name = models.CharField(
        unique=True,
        blank=True,
        max_length=20,
        validators=[UnicodeUsernameValidator()],
        help_text="Public handle or display name (letters, digits, Unicode, @/./+/-/_ allowed)"
    )

    xp = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
