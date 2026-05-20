from django.db import models
from apps.users.models import UserProfile
from apps.courses.models import Lesson
from apps.vocabulary.models import Lexeme

# Create your models here.

# Tracks learning progress for each user lesson
class UserLessonProgress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    completed = models.BooleanField(default=False)

    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(str(self.user.display_name) + " - " + str(self.lesson))

# Tracks the progress of a user with respect to a specific lexeme.
class UserLexemeProgress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE)

    # FSRS state
    stability = models.FloatField(default=0.0)
    difficulty = models.FloatField(default=0.0)
    reps = models.IntegerField(default=0)
    lapses = models.IntegerField(default=0)

    due = models.DateTimeField(null=True, blank=True)
    last_review = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "lexeme")
        indexes = [
            models.Index(fields=["user", "due"]),
        ]

