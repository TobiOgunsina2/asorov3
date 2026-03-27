from collections import defaultdict
import random

from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.views import APIView, Response
from django.utils import timezone

from .constants import max_review_items, max_lesson_review_items
from .helpers import get_sentences_for_words
from apps.curriculum.models import Lesson, Unit

from apps.curriculum.serializers import ( 
    LessonSerializer, 
    UnitSerializer,
    ReviewLessonSlideSerializer
)

from apps.grammar.models import Sentence
from apps.profiles.models import Profile
from apps.progress.models import UserIdiomProgress, UserLessonProgress, UserWordProgress
from apps.progress.views import update_progress

# Create your views here.

class UnitList(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonView(APIView):
    def get(self, request, code):
        user = request.user

        # Fetch the lesson with its slides and related content

        lesson = Lesson.objects.prefetch_related(
        "slides__slide_words",
        "slides__slide_phrases",
        "slides__slide_sentences",
        "slides__slide_words__word__related_words",
        "slides__slide_phrases__phrase_words",
        ).get(code=code)

        # Fetch due words for the user and get sentences for them

        due_words = UserWordProgress.objects.filter(
            user=user,
            due__lte=timezone.now()
        ).select_related("word")[:max_lesson_review_items]

        words = [dw.word for dw in due_words]
        review_data = get_sentences_for_words(words, user.difficulty)
        
        # Serialize the review data and lesson data
        review_slides = ReviewLessonSlideSerializer(review_data, many=True).data
        lesson = LessonSerializer(lesson).data

        return Response({"lesson": {**lesson, "review_slides": review_slides}})
    
class PracticeView(APIView):
    def get(self, request):
        user = request.user

        due_words = UserWordProgress.objects.filter(
            user=user,
            due__lte=timezone.now()
        ).select_related("word")[:max_review_items]

        words = [dw.word for dw in due_words]
        review_data = get_sentences_for_words(words, user.difficulty)
        
        # Serialize the review data and lesson data
        review_slides = ReviewLessonSlideSerializer(review_data, many=True).data
        lesson = LessonSerializer(lesson).data

        return Response({"review_words": review_slides})


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
