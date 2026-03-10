from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.language_cms.models import CMSContentMixin
from .phrase import Phrase
from .word import Word
from django.core.exceptions import ValidationError

# Content Mixin adds:
#   draft
#   review
#   published status, 
#   creator tracking, 
#   and internal notes. 
class Sentence(CMSContentMixin, models.Model):
    """
    Sentences have their own text and translation, 
    but also contain words and phrases which can be highlighted in the sentence.
    """
    text = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    # media = GenericRelation(Media)

    # Difficult of a sentence is arbitrary but useful for generation of slides
    difficulty = models.PositiveIntegerField(db_index=True, default=1)


    def __str__(self):
        return self.text

# This is the through model for both phrases and words to sentence. Can be accessed on sentence as sentence.components
# Typing is weak through content_type!!!
class SentenceComponent(models.Model):

    # 1 -> Many Relationship | As Opposed to many to many in Phrase model 
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name="components")

    # Sentence Component can be Phrase || Word
    word = models.ForeignKey(
        Word,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    phrase = models.ForeignKey(
        Phrase,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField()

    # Highlighting inside this component allows user to see hover over part of sentence to see the component's definition 
    highlight_start = models.PositiveIntegerField(null=True, blank=True)
    highlight_end = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["order"]

    @property
    def text(self):
        return self.word.text if self.word else self.phrase.text
    
    # Method to ensure that exactly one of word or phrase is set, and that highlight range is valid if set
    def clean(self):
        if bool(self.word) == bool(self.phrase):
            raise ValidationError(
                "Component must reference exactly one of word or phrase."
            )

        if (
            self.highlight_start is not None
            and self.highlight_end is not None
            and self.highlight_start >= self.highlight_end
        ):
            raise ValidationError("Invalid highlight range.")


# This model allows for quick lookup of which sentences a word is in, without having to go through the SentenceComponent table and check content types.
# Crucial for quick generation of exercises and lessons based on sentences containing certain words. Updated via signals when SentenceComponents are created/updated/deleted.   
class SentenceWordIndex(models.Model):
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name="sentence_words",)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name="sentence_occurrences")

    class Meta:
        unique_together = ("sentence", "word")
        indexes = [
            models.Index(fields=["word"]),
            models.Index(fields=["sentence"]),
        ]