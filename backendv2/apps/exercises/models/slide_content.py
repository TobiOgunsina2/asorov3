"""from django.db import models

from django.db import models
from apps.vocabulary.models.grammatical_construction import Construction
from .slide import LessonSlide 

# Slide Type Models
# These allow extra information to be added to slides to help their type

class MultipleChoiceContent(models.Model):
    slide = models.OneToOneField(LessonSlide, on_delete=models.CASCADE, related_name="mcq_content")
    question = models.CharField(max_length=200, blank=True)
    options = models.JSONField()  # [{"text": "Option 1", "is_correct": True}, ...]

class TrueFalseContent(models.Model):
    slide = models.OneToOneField(LessonSlide, on_delete=models.CASCADE, related_name="tf_content")
    question = models.CharField(max_length=200, blank=True)
    options = models.JSONField()  # [{"text": "Option 1", "is_correct": True}, ...]

class FillInBlankContent(models.Model):
    slide = models.OneToOneField(LessonSlide, on_delete=models.CASCADE, related_name="fill_in_blank_content")
    sentence = models.ForeignKey(Construction, on_delete=models.CASCADE)
    blanks = models.JSONField()  # [{"start": 10, "end": 14}, ...]

class BuildBlockContent(models.Model):
    slide = models.OneToOneField(LessonSlide, on_delete=models.CASCADE, related_name="build_block_content")
    sentence = models.ForeignKey(Construction, on_delete=models.CASCADE)
"""