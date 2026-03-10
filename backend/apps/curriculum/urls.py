from django.urls import path
from . import views


urlpatterns = [
    path('get-units/', views.UnitList.as_view(), name='get-units'),
    path('get-lesson/', views.LessonView.as_view(), name='get-lesson'),
]
