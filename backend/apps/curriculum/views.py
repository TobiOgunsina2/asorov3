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
from apps.profiles.models import Profile
from apps.progress.models import UserIdiomProgress, UserLessonProgress, UserWordProgress
from apps.progress.views import update_progress
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
    def get(self, request, code):
        user = request.user

        try:
            lesson = get_object_or_404(Lesson, code=code)

            # Fetch the lesson with its slides and related content

            slide_words = SlideWord.objects.filter(
                slide__lesson=lesson
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

class PracticeView(APIView):
    def get(self, request):
        user = request.user

        try:
            profile = Profile.objects.get(user=user)
            due_words = UserWordProgress.objects.filter(
                profile=profile,
                due__lte=timezone.now()
            ).select_related("word")[:20]  # Fetch due words for review

            word_ids = set(p.word_id for p in due_words)
            
            components = (
                SentenceComponent
                    .objects
                    .filter(word_id__in=word_ids, sentence__difficulty__lte=profile.xp) # Update to a profile field that tracks overall progress/difficulty
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

            for due_word in due_words:
                if sentence_map[due_word.word_id]:
                    sentence = random.choice(sentence_map[due_word.word_id])

                    lesson_items.append({
                        "type": "review_word",
                        "word": due_word.word,
                        "sentence": sentence,
                    })    

            serialized_items = LessonItemSerializer(lesson_items, many=True).data

            return Response({"review_items": serialized_items})
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=404)

class ExerciseComplete(APIView):
    def post(self, request, code):
        user = request.user

        try:
            profile = Profile.objects.get(user=user)
            
            if(code):
                lesson = get_object_or_404(Lesson, code=code)

                # Mark the lesson as completed for the user
                lesson_progress, created = UserLessonProgress.objects.get_or_create(profile=profile, lesson=lesson)
                lesson_progress.completed = True
                lesson_progress.completed_at = timezone.now()
                lesson_progress.save()

            items = request.data.get('items')
            for item in items:
                if item['type'] == 'review_word':
                    word_id = item['word_id']
                    quality = item['quality']

                    progress = UserWordProgress.objects.get_or_create(profile=profile, word_id=word_id)
                    if progress.last_reviewed:  # If the object was not just created, it will have a last_reviewed timestamp
                        update_progress(progress, quality)
                
                if item['type'] == 'review_idiom':
                    idiom_id = item['idiom_id']
                    quality = item['quality']

                    progress = UserIdiomProgress.objects.get_or_create(user=user, idiom_id=idiom_id)
                    if progress.last_reviewed:  # If the object was not just created, it will have a last_reviewed timestamp
                        update_progress(progress, quality)

            return Response({"message": "Lesson marked as completed"})
        
        except Lesson.DoesNotExist:
            
            return Response({"error": "Lesson not found"}, status=404)
