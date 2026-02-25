from django.db import models
from .word import Word

# Phrases have their own text and contain words which can be highlighted
class Phrase(models.Model):
    text = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    # media = GenericRelation(Media)


    words = models.ManyToManyField(
        Word,
        through="PhraseWord",
        related_name="phrases"
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