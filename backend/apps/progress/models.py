from apps.profiles.models import Profile
from django.db import models
from django.conf import settings
from apps.curriculum.models.lesson import Lesson
from apps.grammar.models.phrase import Phrase
from apps.grammar.models import Word

# Tracks learning progress for each user lesson
class UserLessonProgress(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(str(self.profile.display_name) + " - " + str(self.lesson))

class UserWordProgress(models.Model):
    """
    Tracks the progress of a user with respect to a specific word.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    # FSRS state
    stability = models.FloatField(default=0.0)
    difficulty = models.FloatField(default=0.0)
    reps = models.IntegerField(default=0)
    lapses = models.IntegerField(default=0)

    due = models.DateTimeField(null=True, blank=True)
    last_review = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "word")
        indexes = [
            models.Index(fields=["user", "due"]),
        ]

# This is strictly for idiom use
class UserIdiomProgress(models.Model):
    """
    Tracks the progress of a user with respect to a specific idiom.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idiom = models.ForeignKey(Phrase, limit_choices_to={'is_idiom': True}, on_delete=models.CASCADE)

    # FSRS state
    stability = models.FloatField(default=0.0)
    difficulty = models.FloatField(default=0.0)
    reps = models.IntegerField(default=0)
    lapses = models.IntegerField(default=0)

    due = models.DateTimeField(null=True, blank=True)
    last_review = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "idiom")
        indexes = [
            models.Index(fields=["user", "due"]),
        ]
        