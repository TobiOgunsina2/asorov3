from django.db import models
from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator

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

# Tracks learning progress for lessons
class UserLessonProgress(models.Model):
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(str(self.profile.display_name) + " - " + str(self.lesson))