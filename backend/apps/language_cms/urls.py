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

    # Preview panel
    path("preview/<str:content_type>/<int:pk>/", views.preview, name="preview"),
]
