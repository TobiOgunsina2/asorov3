from django.contrib import admin
from django.apps import apps
# Register your models here.

app_models = apps.get_app_config('curriculum').get_models()


for model in app_models:
    if model.__name__ in ["Unit", "Lesson", "LessonSlide", "LessonGroup", "Media",]:
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            # This prevents errors if you manually registered a model earlier
            pass