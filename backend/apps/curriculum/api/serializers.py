from rest_framework import serializers
from apps.curriculum.models.lesson import Lesson
from apps.curriculum.models.unit import Unit
from apps.grammar.serializers import SentenceSerializer, WordSerializer, PhraseSerializer
from ..models import LessonSlide, SlideWord, SlidePhrase, SlideSentence
from apps.grammar.models import Sentence

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

#Slide Item instead
"""
class SlideItemSerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)
    phrase = PhraseSerializer(read_only=True)
    sentence = SentenceSerializer(read_only=True)


    class Meta:
        model = SlideSentence
        fields = ["id", "word", "phrase","sentence", "order"]
"""

class ReviewSlideSerializer(serializers.Serializer):
    type = serializers.CharField(default="review")
    word = SlideWordSerializer(many=False, read_only=True)
    sentences = SlideSentenceSerializer(many=True)


class LessonSlideSerializer(serializers.ModelSerializer):
    words = SlideWordSerializer(many=True, read_only=True)
    phrases = SlidePhraseSerializer(many=True, read_only=True)
    sentences = SlideSentenceSerializer(many=True, read_only=True)

    class Meta:
        model = LessonSlide
        fields = [
            "id", "lesson", "order", "slide_type",
            "words", "phrases", "sentences",
        ]

class LessonSerializer(serializers.ModelSerializer):
    slides = LessonSlideSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "title", "code", "description", "order", "difficulty", "slides"]
    
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