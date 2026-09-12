from django.urls import path
from . import views


urlpatterns = [
    path('complete-exercise/<str:code>/', views.ExerciseComplete.as_view(), name='complete-exercise'),
]
