from django.contrib import admin

from apps.progress.models import UserLessonProgress, UserWordProgress, UserIdiomProgress

# Register your models here.

admin.site.register(UserWordProgress)
admin.site.register(UserIdiomProgress)
admin.site.register(UserLessonProgress)


