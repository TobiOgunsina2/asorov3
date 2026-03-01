# language_cms/urls.py
from django.urls import path
from . import views

app_name = "cms"

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),

    # Words
    path("words/", views.word_list, name="word_list"),
    path("words/create/", views.word_create, name="word_create"),
    path("words/<int:pk>/edit/", views.word_edit, name="word_edit"),
    path("words/<int:pk>/delete/", views.word_delete, name="word_delete"),
    path("words/<int:pk>/status/", views.word_status, name="word_status"),

    # Phrases
    path("phrases/", views.phrase_list, name="phrase_list"),
    path("phrases/create/", views.phrase_create, name="phrase_create"),
    path("phrases/<int:pk>/edit/", views.phrase_edit, name="phrase_edit"),
    path("phrases/<int:pk>/delete/", views.phrase_delete, name="phrase_delete"),

    # Sentences
    path("sentences/", views.sentence_list, name="sentence_list"),
    path("sentences/create/", views.sentence_create, name="sentence_create"),
    path("sentences/<int:pk>/edit/", views.sentence_edit, name="sentence_edit"),
    path("sentences/<int:pk>/delete/", views.sentence_delete, name="sentence_delete"),

    # Units
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/<int:pk>/', views.unit_detail, name='unit_detail'),
    path('units/<int:pk>/edit/', views.unit_edit, name='unit_edit'),
    path('units/<int:pk>/delete/', views.unit_delete, name='unit_delete'),

    # LessonGroups
    path('units/<int:unit_pk>/groups/create/', views.lesson_group_create, name='lesson_group_create'),
    path('groups/<int:pk>/edit/', views.lesson_group_edit, name='lesson_group_edit'),
    path('groups/<int:pk>/delete/', views.lesson_group_delete, name='lesson_group_delete'),

    # Lessons
    path('groups/<int:group_pk>/lessons/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:pk>/delete/', views.lesson_delete, name='lesson_delete'),

    # Slides
    path('lessons/<int:lesson_pk>/slides/create/', views.slide_create, name='slide_create'),
    path('slides/<int:pk>/', views.slide_edit, name='slide_edit'),
    path('slides/<int:pk>/delete/', views.slide_delete, name='slide_delete'),
    path('slides/<int:pk>/reorder/', views.slide_reorder, name='slide_reorder'),
    path('slides/content-panel/', views.slide_content_panel, name='slide_content_panel'),

    # Preview panel
    path("preview/<str:content_type>/<int:pk>/", views.preview, name="preview"),
]
