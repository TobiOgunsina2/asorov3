from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# A sentence is composed of words and phrases
class Sentence(models.Model):
    text = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)

    def __str__(self):
        return self.text

# This is the through model for both phrases and words to sentence. Can be accessed on sentence as sentence.components
class SentenceComponent(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name="components")

    # GenericForeignKey to Word or Phrase
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    order = models.PositiveIntegerField()

    # Highlighting inside this component allows user to see hover over part of sentence to see the component's definition 
    highlight_start = models.PositiveIntegerField(null=True, blank=True)
    highlight_end = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["order"]

"""
For further reference, lesson models should be serialized as such to minimize queries:

from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch

word_type = ContentType.objects.get_for_model(Word)
phrase_type = ContentType.objects.get_for_model(Phrase)

LessonSlide.objects.prefetch_related(
    Prefetch(
        "sentence__components",
        queryset=SentenceComponent.objects.select_related("content_type").prefetch_related("content_object__phrase_words__word")
    )
)

"""