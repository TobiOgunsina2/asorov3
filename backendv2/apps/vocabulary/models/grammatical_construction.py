from django.db import models
from apps.vocabulary.models.lexeme import Lexeme, LexemeVariant
from django.core.exceptions import ValidationError

# Create your models here.

class ConstructionType(models.TextChoices):
    IDIOM = 'Idiom'
    PATTERN = "pattern"
    PHRASE = 'Phrase'
    SENTENCE = 'Sentence'

class ComponentDifficulty(models.IntegerChoices):
    A1 = 1
    A2 = 2
    B1 = 3
    B2 = 4
    C1 = 5
    C2 = 6


# Construction component outlines more advanced grammatical structures
# E.g Idioms, Phrases, Sentences etc.
# They are built from multiple lexemes and can be built from other constructions (for nested constructions).
# E.g Oruko mi ni Tobi

class Construction(models.Model):
    native_text = models.CharField(max_length=255)
    
    normalized_text = models.TextField(
        db_index=True
    )

    construction_type = models.CharField(max_length=255, choices=ConstructionType.choices)

    translation = models.CharField(max_length=255, blank=True, null=True)

    notes = models.TextField(blank=True)

    difficulty = models.PositiveSmallIntegerField(
        default=1,
        choices=ComponentDifficulty.choices,
        db_index=True
    )

    is_reviewable = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.native_text

    class Meta:
        ordering = ['-created_at']


# The individual components that make up a construction. This can be a lexeme or another construction (for nested constructions).
class ConstructionComponent(models.Model):
    
    # Parent construction that this component belongs to
    construction = models.ForeignKey(
        Construction,
        on_delete=models.CASCADE,
        related_name="components"
    )

    lexeme = models.ForeignKey(
        LexemeVariant,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    child_construction = models.ForeignKey(
        Construction,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    position = models.PositiveIntegerField()

    grammatical_role = models.CharField(
        max_length=50,
        blank=True
    )

    highlight_start = models.PositiveIntegerField(null=True, blank=True)
    highlight_end = models.PositiveIntegerField(null=True, blank=True)


    class Meta:
        ordering = ["position"]

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


class ConstructionLexeme(models.Model):

    construction = models.ForeignKey(
        Construction,
        on_delete=models.CASCADE,
        related_name="lexeme_index"
    )

    lexeme = models.ForeignKey(
        Lexeme,
        on_delete=models.CASCADE
    )

    is_direct = models.BooleanField(default=True)

    depth = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = (
            "construction",
            "lexeme",
            "depth",
        )

        indexes = [
            models.Index(
                fields=["lexeme"]
            ),
            models.Index(
                fields=["construction"]
            ),
        ]