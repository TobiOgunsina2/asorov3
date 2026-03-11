from django.urls import path
from . import views


urlpatterns = [
    path('get-units/', views.UnitList.as_view(), name='get-units'),
    path('get-lesson/<str:code>/', views.LessonView.as_view(), name='get-lesson'),
    path('get-practice/', views.PracticeView.as_view(), name='get-practice'),
    path('complete-exercise/<str:code>/', views.ExerciseComplete.as_view(), name='complete-exercise'),
]
