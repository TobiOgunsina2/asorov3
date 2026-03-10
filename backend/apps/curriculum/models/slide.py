from django.db import models
from .lesson import Lesson
from apps.grammar.models import Phrase, Sentence, Word 

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

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.slide_type}: {self.lesson.title} (#{self.order})"
    
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
