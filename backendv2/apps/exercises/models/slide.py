from django.db import models
from apps.courses.models.Lesson import Lesson
from apps.vocabulary.models.lexeme import Lexeme 
from django.db.models import Prefetch


# Query Set for easier prefetching
"""class SlideQuerySet(models.QuerySet):

    def with_slide_content(self):
        return self.prefetch_related(
            Prefetch(
                "slide_content__lexemes",
                queryset=Lexeme.objects.select_related(
                    "word"
                ).prefetch_related(
                    Prefetch("word__related_words")
                ),
            )
        )
"""

class SlideType(models.TextChoices):
    INTRO = "Intro", "Intro"
    MULTIPLE_CHOICE = "MultipleChoice", "MultipleChoice"
    TRUE_FALSE = "TrueFalse", "TrueFalse"
    BUILD_BLOCK = "BuildBlock", "BuildBlock"
    FILL_IN_BLANK = "FillInBlank", "FillInBlank"
    MATCH_PAIRS = "MatchPairs", "MatchPairs"
    TYPE_WORD = "TypeWord", "TypeWord"
    CROSSWORD = "Crossword", "Crossword"
    TONE_MARKING = "ToneMarking", "ToneMarking"
    SPEAKING = "Speaking", "Speaking"
    SKETCH = "Sketch", "Sketch"
    TEXT_RESPONSE = "TextResponse", "TextResponse"
    READ_PARAGRAPH = "ReadParagraph", "ReadParagraph"
    RANDOM = "Random", "Random"


# The lesson slide model is a base model which can be improved by one of the slide type models to add augmentations
class Slide(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="slides")
    
    slide_type = models.CharField(
        max_length=50,
        choices=SlideType.choices,
        default=SlideType.INTRO
    )

    order = models.PositiveIntegerField()

    # objects = SlideQuerySet.as_manager()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.slide_type}: {self.lesson.title} (#{self.order})"

