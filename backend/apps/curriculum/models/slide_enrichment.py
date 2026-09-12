from django.db import models
from apps.grammar.models import Sentence
from .slide import LessonSlide 


# Slide Type Models
# These allow extra information to be added to slides to help their type

class MultipleChoiceContent(models.Model):
    slide = models.OneToOneField(LessonSlide, on_delete=models.CASCADE, related_name="mc_content")
    question = models.CharField(max_length=200, blank=True)
    options = models.JSONField()  # [{"text": "Option 1", "is_correct": True}, ...]

class TrueFalseContent(models.Model):
    slide = models.OneToOneField(LessonSlide, on_delete=models.CASCADE, related_name="tf_content")
    question = models.CharField(max_length=200, blank=True)
    options = models.JSONField()  # [{"text": "Option 1", "is_correct": True}, ...]

class FillInBlankContent(models.Model):
    slide = models.OneToOneField(LessonSlide, on_delete=models.CASCADE, related_name="fib_content")
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    blanks = models.JSONField()  # [{"start": 10, "end": 14}, ...]

class BuildBlockContent(models.Model):
    slide = models.OneToOneField(LessonSlide, on_delete=models.CASCADE, related_name="bb_content")
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    word_order = models.JSONField(blank=True, null=True)  # allows shuffling words for exercises