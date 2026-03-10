from collections import defaultdict
import random

from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from apps.curriculum.models.lesson import Lesson
from apps.curriculum.models.slide import SlideWord
from apps.curriculum.models.unit import Unit

from apps.curriculum.serializers import (
    LessonItemSerializer, 
    LessonSerializer, 
    UnitSerializer
)

from apps.grammar.models.sentence import SentenceComponent
from apps.progress.models import UserWordProgress
from .const import max_review_items
from rest_framework.views import APIView, Response
from django.utils import timezone
from apps.grammar.models import Sentence

# Create your views here.

class UnitList(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonView(APIView):
    def get(self, request):
        user = request.user
        lesson_id = request.query_params.get("lesson_id")

        try:
            lesson = get_object_or_404(Lesson, id=lesson_id)

            # Fetch the lesson with its slides and related content

            slide_words = SlideWord.objects.filter(
                slide__lesson_id=lesson_id
                ).select_related("word")

            due_words = UserWordProgress.objects.filter(
                user=user,
                due__lte=timezone.now()
            ).select_related("word")[:max_review_items]

            word_ids = set(sw.word_id for sw in slide_words)
            word_ids.update(p.word_id for p in due_words)
            
            components = (
                SentenceComponent
                    .objects
                    .filter(word_id__in=word_ids, sentence__difficulty__lte=lesson.difficulty)
                    .select_related("word", "sentence")
                    .distinct()
            )  # Fetch sentences that include these words

            sentence_ids = [sc.sentence_id for sc in components]

            sentences = Sentence.objects.in_bulk(sentence_ids)  # Fetch sentences in bulk

            # Defaultdict to map word_id to sentences that include it
            sentence_map = defaultdict(list)

            for component in components:
                # Map word_id to sentences that include it
                sentence_map[component.word_id].append(sentences[component.sentence_id])
            
            lesson_items = []

            for sw in slide_words:
                sentence = None
                
                # Add random sentences for slide words, and review sentences for due words
                if sw.slide.slide_type == "Random":
                    # No point of checking sentence_map if the slide is not random
                    if sentence_map[sw.word_id]:
                        sentence = random.choice(sentence_map[sw.word_id])
                
                # All lesson slides are added under here
                lesson_items.append({
                    "type": "slide_word",
                    "slide": sw.slide,
                    "word": sw.word,
                    "sentence": sentence,
                })

            for due_word in due_words:
                if sentence_map[due_word.word_id]:
                    sentence = random.choice(sentence_map[due_word.word_id])

                    lesson_items.append({
                        "type": "review_word",
                        "word": due_word.word,
                        "sentence": sentence,
                    })    

            serialized_items = LessonItemSerializer(lesson_items, many=True).data
            lesson = LessonSerializer(lesson).data

            return Response({"lesson": {**lesson, "items": serialized_items}})
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=404)
        