from django.db import models
from apps.vocabulary.models.lexeme import Lexeme, LexemeVariant
from django.core.exceptions import ValidationError
from django.db.models import Max

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


# The individual components that make up a construction. 
# This can be a lexeme or another construction (for nested constructions).
class ConstructionComponent(models.Model):
    
    # Parent construction that this component belongs to
    construction = models.ForeignKey(
        Construction,
        on_delete=models.CASCADE,
        related_name="components"
    )

    lexeme = models.ForeignKey(
        Lexeme,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    lexeme_variant = models.ForeignKey(
        LexemeVariant, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
    )

    child_construction = models.ForeignKey(
        Construction,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    position = models.PositiveIntegerField()

    def __str__(self):
        target = self.lexeme or self.child_construction
        return f"{self.construction} [{self.position}] - {target}"


    class Meta:
        ordering = ["position"]

        constraints = [
            models.UniqueConstraint(
                fields=['construction', 'position'], 
                name='unique_component_position_per_construction'
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(lexeme__isnull=False, child_construction__isnull=True)
                    | models.Q(lexeme__isnull=True, child_construction__isnull=False)
                ),
                name="component_xor_lexeme_or_construction",
            )
        ]

    # Method to ensure that a component cannot point to both a 
    # Lexeme and a child Construction, and must point to at least one of them.
    def clean(self):     
        if self.lexeme_variant and not self.lexeme:
            self.lexeme = self.lexeme_variant.lexeme

        if self.lexeme and self.child_construction:
            raise ValidationError("A component cannot point to both a Lexeme and a child Construction.")
        
        if not self.lexeme and not self.child_construction:
            raise ValidationError("A component must point to either a Lexeme or a child Construction.")
        
        if self.lexeme_variant and self.lexeme_variant.lexeme_id != self.lexeme_id:
            raise ValidationError("The selected LexemeVariant does not belong to the selected Lexeme.")

    def save(self, *args, **kwargs):
        if self.lexeme_variant and not self.lexeme:
            self.lexeme = self.lexeme_variant.lexeme

        if self.position is None:
            # Look up the maximum position within this construction
            last_position = ConstructionComponent.objects.filter(
                construction=self.construction
            ).aggregate(Max('position'))['position__max']
            
            # If last_position is None (first item), fallback to 0, then add 1
            self.position = (last_position or 0) + 1
        
        self.full_clean()
        super().save(*args, **kwargs)



# Highlights allow users to see definitions of parts of a construction in context.
class Highlight(models.Model):
    construction_component = models.ForeignKey(
        ConstructionComponent,
        on_delete=models.CASCADE,
        related_name="highlights"
    )

    start_index = models.PositiveIntegerField()
    end_index = models.PositiveIntegerField()

    def clean(self):
        if (
            self.start_index is not None
            and self.end_index is not None
            and self.start_index >= self.end_index
        ):
            raise ValidationError("Invalid highlight range.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# Flattened map linking constructions to all contained lexemes and variants.
# Enables fast context lookups for SRS review loops.

class ConstructionLexeme(models.Model):

    construction = models.ForeignKey(
        Construction,
        on_delete=models.CASCADE,
        related_name="lexeme_index"
    )

    lexeme = models.ForeignKey(
        Lexeme,
        on_delete=models.CASCADE,
        related_name="construction_index"
    )

    lexeme_variant = models.ForeignKey(
        LexemeVariant, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name="construction_index"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['construction', 'lexeme', 'lexeme_variant'], 
                name='unique_construction_lexeme_variant_index'
            )
        ]

        indexes = [
            models.Index(fields=["lexeme", "construction"]),
            models.Index(fields=["lexeme_variant", "construction"]),
        ]