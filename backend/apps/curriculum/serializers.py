from random import random

from rest_framework import serializers

from apps.curriculum.models.lesson import Lesson
from apps.curriculum.models.unit import Unit
from apps.grammar.serializers import SentenceSerializer, WordSerializer, PhraseSerializer
from .models import LessonSlide, SlideWord, SlidePhrase, SlideSentence
from apps.grammar.models import Sentence  # adjust import path as needed


class SlideWordSerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)
    class Meta:
        model = SlideWord
        fields = ["id", "word", "order"]


class SlidePhraseSerializer(serializers.ModelSerializer):
    phrase = PhraseSerializer(read_only=True)

    class Meta:
        model = SlidePhrase
        fields = ["id", "phrase", "order"]


class SlideSentenceSerializer(serializers.ModelSerializer):
    sentence = SentenceSerializer(read_only=True)

    class Meta:
        model = SlideSentence
        fields = ["id", "sentence", "order"]


class LessonSlideSerializer(serializers.ModelSerializer):
    slide_words = SlideWordSerializer(many=True, read_only=True)
    slide_phrases = SlidePhraseSerializer(many=True, read_only=True)
    slide_sentences = SlideSentenceSerializer(many=True, read_only=True)

    class Meta:
        model = LessonSlide
        fields = [
            "id", "lesson", "order", "slide_type",
            "slide_words", "slide_phrases", "slide_sentences",
        ]

class LessonItemSerializer(serializers.Serializer):
    type = serializers.CharField()  # "slide_word" or "review_word"
    slide = LessonSlideSerializer(required=False)
    word = WordSerializer()
    sentence = SentenceSerializer(required=False, many=True)   

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "order", "difficulty", "slides"]
    
class LessonGroupSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ["id", "title", "description", "lessons"]

class UnitSerializer(serializers.ModelSerializer):
    lesson_groups = LessonGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ["id", "title", "description", "lesson_groups"]