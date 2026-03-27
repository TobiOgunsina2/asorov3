from rest_framework import serializers
from apps.curriculum.models.lesson import Lesson
from apps.curriculum.models.unit import Unit
from apps.grammar.serializers import SentenceSerializer, WordSerializer, PhraseSerializer
from .models import LessonSlide, SlideWord, SlidePhrase, SlideSentence
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

class ReviewLessonSlideSerializer(serializers.Serializer):
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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user

        if instance.slide_type == "Random" and user and instance.words.exists():
            first_word = instance.words.first()
            sentence = self._get_random_sentence(first_word.word, user.difficulty)
            data['injected_sentence'] = SentenceSerializer(sentence).data if sentence else None
        return data
    
    def _get_random_sentence(self, word, max_difficulty):
        return (
            Sentence.objects
            .filter(
                components__word=word,
                difficulty__lt=max_difficulty,
            )
            .order_by('?')  # random at DB level
            .prefetch_related('components__word', 'components__phrase')  # prefetch related for serialization
            .first()
        )

class LessonSerializer(serializers.ModelSerializer):
    slides = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ["id", "title", "code", "description", "order", "difficulty", "slides"]
    
    def get_slides(self, lesson):
        user = self.context['request'].user
        
        slides = list(lesson.slides.all())
        data = LessonSlideSerializer(slides, many=True, context=self.context).data
        
        return data
    
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