from django.db import models
from .lesson import Lesson
from apps.grammar.models import Phrase, Sentence, Word 
from django.db.models import Prefetch

# Query Set for easier prefetching
class SlideQuerySet(models.QuerySet):

    def with_slide_content(self):
        return self.prefetch_related(
            Prefetch(
                "slide_words",
                queryset=SlideWord.objects.select_related(
                    "word"
                ).prefetch_related(
                    Prefetch("word__related_words")
                ),
            ),
            Prefetch(
                "slide_phrases",
                queryset=SlidePhrase.objects.prefetch_related(
                    "phrase_words"
                ),
            ),
            Prefetch(
                "slide_sentences",
                queryset=SlideSentence.objects.prefetch_related(
                    "sentence_words",
                    "sentence_phrases"
                ),
            ),
        )

# The lesson slide model is a base model which can be improved by one of the slide type models to add augmentations
class LessonSlide(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="slides")
    order = models.FloatField()  # Float field allows inserting slides anywhere (e.g 1.0, 1.5, 2.0)
    slide_type = models.CharField(
        max_length=50,
        choices=[
            ("Intro", "Intro"),
            ("MultipleChoice", "MultipleChoice"),
            ("TrueFalse", "TrueFalse"),
            ("BuildBlock", "BuildBlock"),
            ("FillInBlank", "FillInBlank"),
            ("MatchPairs", "MatchPairs"),
            ("TypeWord", "TypeWord"),
            ("Crossword", "Crossword"),
            ("ToneMarking", "ToneMarking"),
            ("Speaking", "Speaking"),
            ("Sketch", "Sketch"),
            ("TextResponse", "TextResponse"),
            ("ReadParagraph", "ReadParagraph"),
            ("Random", "Random"),
        ],
    )

    objects = SlideQuerySet.as_manager()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.slide_type}: {self.lesson.title} (#{self.order})"


# These models link the lesson slides to specific words, phrases, and sentences that are relevant for the exercises.
class SlideWord(models.Model):
    slide = models.ForeignKey(LessonSlide, on_delete=models.CASCADE, related_name="slide_words")
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    order = models.FloatField(null=True, blank=True)  # if order matters for the exercise

class SlidePhrase(models.Model):
    slide = models.ForeignKey(LessonSlide, on_delete=models.CASCADE, related_name="slide_phrases")
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    order = models.FloatField(null=True, blank=True)

class SlideSentence(models.Model):
    slide = models.ForeignKey(LessonSlide, on_delete=models.CASCADE, related_name="slide_sentences")
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    order = models.FloatField(null=True, blank=True)


class SlideItem(models.Model):
    slide = models.ForeignKey(LessonSlide, on_delete=models.CASCADE, related_name="slide_items")
    
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)

    order = models.FloatField(null=True, blank=True)  # if order matters for the exercise
