from django.db import models
from .unit import Unit

# Having lesson group allows concepts to be split up into multiple parts without
# taking up lot's of screen real estate on the front end. Makes lessons more digestable
class LessonGroup(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lesson_groups")
    title = models.CharField(max_length=200)
    order = models.FloatField()

# A lesson can be the only one in it's group
class Lesson(models.Model):
    group = models.ForeignKey(LessonGroup, null=True, blank=True, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.FloatField()

