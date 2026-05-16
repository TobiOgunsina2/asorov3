from django.db import models

# Create your models here.

# This model represents a single lexeme, which is the basic unit of meaning in a language. 
# It includes fields for the lemma (the canonical form of the word)

class Lexeme(models.Model):
    lemma = models.CharField(max_length=255)
    normalized_lemma = models.CharField(max_length=255)

    tone_pattern = models.CharField(max_length=255) # Possibly Expendable

    translation = models.CharField(max_length=255)

    notes = models.TextField(blank=True, null=True)

    frequency_rank = models.IntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lemma

    class Meta:
        ordering = ['-created_at']

# This model represents a variant of a lexeme, which can include different forms of the word
# E.g the verb ni can be the preoposition "in" or can be the verb "to be"

class LexemeVariant(models.Model):
    lexeme = models.ForeignKey(Lexeme, related_name='variants', on_delete=models.CASCADE)
    variant = models.CharField(max_length=255)

    part_of_speech = models.CharField(max_length=255, blank=True, null=True)

    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.variant