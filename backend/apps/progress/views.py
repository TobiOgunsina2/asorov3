from django.shortcuts import get_object_or_404
from django.utils import timezone
from apps.curriculum.models.lesson import Lesson
from apps.profiles.models import Profile
from apps.progress.models import UserIdiomProgress, UserLessonProgress, UserWordProgress
from apps.progress.helpers import update_progress
from rest_framework.views import APIView, Response


# Create your views here.

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

