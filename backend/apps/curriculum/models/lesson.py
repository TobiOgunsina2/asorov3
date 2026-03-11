from django.db import models
from .unit import Unit
from apps.curriculum.constants import ID_LENGTH
import string
import secrets

def generate_unique_short_code():
    """
    Generates a unique 6-character alphanumeric code for Lesson.
    Retries until a unique code is found.
    """

    ALPHANUMERIC_CHARS = string.ascii_lowercase + string.digits

    while True:
        # Generate a random 6-character string
        code = ''.join(secrets.choice(ALPHANUMERIC_CHARS) for i in range(ID_LENGTH))
        # Check if this code already exists in the database
        if not Lesson.objects.filter(code=code).exists():
            return code

# Having lesson group allows concepts to be split up into multiple parts without
# taking up lot's of screen real estate on the front end. Makes lessons more digestable
class LessonGroup(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lesson_groups")
    title = models.CharField(max_length=200)
    order = models.FloatField()

    def __str__(self):
        return str("Lesson Group - " + self.title)


# A lesson can be the only one in it's group
class Lesson(models.Model):
    group = models.ForeignKey(LessonGroup, null=True, blank=True, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=ID_LENGTH, unique=True, default=generate_unique_short_code, editable=False)
    description = models.TextField(blank=True)
    order = models.FloatField()

    difficulty = models.IntegerField(default=1)  # New field to indicate lesson difficulty

    def __str__(self):
        return str("Lesson - " + self.title)


