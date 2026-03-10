from django.db import models
from .word import Word
from apps.language_cms.models import CMSContentMixin


# Content Mixin adds:
#   draft
#   review
#   published status, 
#   creator tracking, 
#   and internal notes. 
class Phrase(CMSContentMixin, models.Model):
    """
    Phrases have their own text and contain words which can be highlighted in the phrase. 
    This allows for phrases to have idiomatic translations which don't directly map word-for-word, 
    while still allowing users to see the individual words and their definitions.
    """
    text = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    # media = GenericRelation(Media)

    words = models.ManyToManyField(
        Word,
        through="PhraseWord",
        related_name="phrases"
    )

    # Allows for true idioms that don't have a direct word-for-word translation to be added for review.
    is_idiom = models.BooleanField(
        default=False,
        help_text="Check if this phrase is a true idiom (non-literal translation)",
    )

    def __str__(self):
        return self.text

# The through table that allows for ordering words in a phrase
class PhraseWord(models.Model):
    phrase = models.ForeignKey(
        Phrase,
        on_delete=models.CASCADE,
        related_name="phrase_words"
    )
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.text