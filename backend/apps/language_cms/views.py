# language_cms/views.py
#
# Replace the mock querysets below with real ORM queries once you wire up your models.
# All views check for the "content_architect" group (or is_staff) before allowing access.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone

from apps.grammar.models import Word, Phrase, Sentence
from .models import PublishStatus

from .forms import WordForm, PhraseForm, SentenceForm, SearchFilterForm
from .curriculum_views import *

def is_architect(user):
    return user.is_staff or user.groups.filter(name="content_architect").exists()

architect_required = user_passes_test(is_architect, login_url="/accounts/login/")


# ── Dashboard ────────────────────────────────────────────────────────────────

@login_required
@architect_required
def dashboard(request):
    # Slide type breakdown — e.g. {"MultipleChoice": 4, "Intro": 2}
    slide_type_breakdown = dict(
        LessonSlide.objects
            .values_list("slide_type")
            .annotate(count=Count("id"))
            .order_by("-count")
            .values_list("slide_type", "count")
    )

    stats = {
        "units":         Unit.objects.count(),
        "lesson_groups": LessonGroup.objects.count(),
        "lessons":       Lesson.objects.count(),
        "slides":        LessonSlide.objects.count(),
        "slide_type_breakdown": slide_type_breakdown,
        "words": {
            "total":     Word.objects.count(),
            "published": Word.objects.filter(status="published").count(),
            "draft":     Word.objects.filter(status="draft").count(),
        },
        "phrases": {
            "total":     Phrase.objects.count(),
            "published": Phrase.objects.filter(status="published").count(),
            "draft":     Phrase.objects.filter(status="draft").count(),
        },
        "sentences": {
            "total":     Sentence.objects.count(),
            "published": Sentence.objects.filter(status="published").count(),
            "draft":     Sentence.objects.filter(status="draft").count(),
        },
    }

    recent_lessons = (
        Lesson.objects
            .select_related("group__unit")
            .prefetch_related("slides")
            .order_by("-id")[:6]
    )

    recent_words = Word.objects.order_by("-updated_at")[:6]

    return render(request, "cms/dashboard.html", {
        "stats": stats,
        "recent_lessons": recent_lessons,
        "recent_words": recent_words,
    })
# ── Words ────────────────────────────────────────────────────────────────────

@login_required
@architect_required
def word_list(request):
    qs = Word.objects.select_related("created_by").order_by("-updated_at")
    form = SearchFilterForm(request.GET)
    q = request.GET.get("q", "")
    status = request.GET.get("status", "")
    pos = request.GET.get("pos", "")
    if q:
        qs = qs.filter(Q(text__icontains=q) | Q(translation__icontains=q))
    if status:
        qs = qs.filter(status=status)
    if pos:
        qs = qs.filter(part_of_speech=pos)
    paginator = Paginator(qs, 25)
    page = paginator.get_page(request.GET.get("page", 1))
    template = "cms/partials/word_rows.html" if request.headers.get("HX-Request") else "cms/word_list.html"
    return render(request, template, {"page": page, "form": form, "content_type": "word"})


@login_required
@architect_required
def word_create(request):
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word = Word.objects.create(
                text=form.cleaned_data["text"],
                translation=form.cleaned_data["translation"],
                part_of_speech=form.cleaned_data["part_of_speech"],
                notes=form.cleaned_data["notes"],
                status=form.cleaned_data["status"],
                related_words=form.cleaned_data["related_words"],
                created_by=request.user,
            )
            messages.success(request, "Word created successfully.")
            if request.headers.get("HX-Request"):
                return HttpResponse(status=204, headers={"HX-Trigger": "contentChanged"})
            return redirect("cms:word_list")
    else:
        form = WordForm()
    template = "cms/partials/word_form.html" if request.headers.get("HX-Request") else "cms/word_form.html"
    return render(request, template, {"form": form, "action": "Create", "content_type": "word"})


@login_required
@architect_required
def word_edit(request, pk):
    word = get_object_or_404(Word, pk=pk)
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word.text = form.cleaned_data["text"]
            word.translation = form.cleaned_data["translation"]
            word.part_of_speech = form.cleaned_data["part_of_speech"]
            word.notes = form.cleaned_data["notes"]
            word.status = form.cleaned_data["status"]
            word.related_words = form.cleaned_data["related_words"]
            word.updated_at = timezone.now()
            word.save(update_fields=["text", "translation", "part_of_speech", "notes","related_words", "status", "updated_at"])
            messages.success(request, "Word updated.")
            if request.headers.get("HX-Request"):
                return HttpResponse(status=204, headers={"HX-Trigger": "contentChanged"})
            return redirect("cms:word_list")
    else:
        form = WordForm(initial={
            "text": word.text,
            "translation": word.translation,
            "part_of_speech": word.part_of_speech,
            "related_words": word.related_words.all(),
        })
        form.fields["related_words"].queryset = Word.objects.exclude(pk=word.pk)
    template = "cms/partials/word_form.html" if request.headers.get("HX-Request") else "cms/word_form.html"
    return render(request, template, {"form": form, "action": "Edit", "object": word, "content_type": "word"})


@login_required
@architect_required
@require_POST
def word_delete(request, pk):
    get_object_or_404(Word, pk=pk).delete()
    messages.success(request, "Word deleted.")
    if request.headers.get("HX-Request"):
        return HttpResponse(status=200, headers={"HX-Trigger": "contentChanged"})
    return redirect("cms:word_list")


@login_required
@architect_required
@require_POST
def word_status(request, pk):
    """Quick status toggle from list view."""
    new_status = request.POST.get("status")
    word = get_object_or_404(Word, pk=pk)
    word.status = new_status; word.save(update_fields=["status", "updated_at"])
    if request.headers.get("HX-Request"):
        return HttpResponse(status=204, headers={"HX-Trigger": "contentChanged"})
    return redirect("cms:word_list")


# ── Phrases ──────────────────────────────────────────────────────────────────

@login_required
@architect_required
def phrase_list(request):
    qs = []
    form = SearchFilterForm(request.GET)
    paginator = Paginator(qs, 25)
    page = paginator.get_page(request.GET.get("page", 1))
    template = "cms/partials/phrase_rows.html" if request.headers.get("HX-Request") else "cms/phrase_list.html"
    return render(request, template, {"page": page, "form": form, "content_type": "phrase"})


@login_required
@architect_required
def phrase_create(request):
    if request.method == "POST":
        form = PhraseForm(request.POST)
        if form.is_valid():
            messages.success(request, "Phrase created successfully.")
            if request.headers.get("HX-Request"):
                return HttpResponse(status=204, headers={"HX-Trigger": "contentChanged"})
            return redirect("cms:phrase_list")
    else:
        form = PhraseForm()
    template = "cms/partials/phrase_form.html" if request.headers.get("HX-Request") else "cms/phrase_form.html"
    # Pass available words for the word-picker
    words = Word.objects.filter(status="published").order_by("text")
    words = []
    return render(request, template, {"form": form, "action": "Create", "words": words, "content_type": "phrase"})


@login_required
@architect_required
def phrase_edit(request, pk):
    phrase = None
    if request.method == "POST":
        form = PhraseForm(request.POST)
        if form.is_valid():
            messages.success(request, "Phrase updated.")
            if request.headers.get("HX-Request"):
                return HttpResponse(status=204, headers={"HX-Trigger": "contentChanged"})
            return redirect("cms:phrase_list")
    else:
        form = PhraseForm()
    words = []
    template = "cms/partials/phrase_form.html" if request.headers.get("HX-Request") else "cms/phrase_form.html"
    return render(request, template, {"form": form, "action": "Edit", "object": phrase, "words": words, "content_type": "phrase"})


@login_required
@architect_required
@require_POST
def phrase_delete(request, pk):
    messages.success(request, "Phrase deleted.")
    if request.headers.get("HX-Request"):
        return HttpResponse(status=200, headers={"HX-Trigger": "contentChanged"})
    return redirect("cms:phrase_list")


# ── Sentences ────────────────────────────────────────────────────────────────

@login_required
@architect_required
def sentence_list(request):
    qs = []
    form = SearchFilterForm(request.GET)
    paginator = Paginator(qs, 25)
    page = paginator.get_page(request.GET.get("page", 1))
    template = "cms/partials/sentence_rows.html" if request.headers.get("HX-Request") else "cms/sentence_list.html"
    return render(request, template, {"page": page, "form": form, "content_type": "sentence"})


@login_required
@architect_required
def sentence_create(request):
    if request.method == "POST":
        form = SentenceForm(request.POST)
        if form.is_valid():
            messages.success(request, "Sentence created successfully.")
            if request.headers.get("HX-Request"):
                return HttpResponse(status=204, headers={"HX-Trigger": "contentChanged"})
            return redirect("cms:sentence_list")
    else:
        form = SentenceForm()
    words = []
    phrases = []
    template = "cms/partials/sentence_form.html" if request.headers.get("HX-Request") else "cms/sentence_form.html"
    return render(request, template, {"form": form, "action": "Create", "words": words, "phrases": phrases, "content_type": "sentence"})


@login_required
@architect_required
def sentence_edit(request, pk):
    sentence = None
    if request.method == "POST":
        form = SentenceForm(request.POST)
        if form.is_valid():
            messages.success(request, "Sentence updated.")
            if request.headers.get("HX-Request"):
                return HttpResponse(status=204, headers={"HX-Trigger": "contentChanged"})
            return redirect("cms:sentence_list")
    else:
        form = SentenceForm()
    words = []
    phrases = []
    template = "cms/partials/sentence_form.html" if request.headers.get("HX-Request") else "cms/sentence_form.html"
    return render(request, template, {"form": form, "action": "Edit", "object": sentence, "words": words, "phrases": phrases, "content_type": "sentence"})


@login_required
@architect_required
@require_POST
def sentence_delete(request, pk):
    messages.success(request, "Sentence deleted.")
    if request.headers.get("HX-Request"):
        return HttpResponse(status=200, headers={"HX-Trigger": "contentChanged"})
    return redirect("cms:sentence_list")


# ── Preview ──────────────────────────────────────────────────────────────────

@login_required
@architect_required
def preview(request, content_type, pk):
    """Renders a preview panel for Word, Phrase or Sentence."""
    obj = None
    if content_type == "word":   obj = get_object_or_404(Word, pk=pk)
    elif content_type == "phrase": obj = get_object_or_404(Phrase, pk=pk)
    elif content_type == "sentence": obj = get_object_or_404(Sentence, pk=pk)
    template = "cms/partials/preview.html"
    return render(request, template, {"obj": obj, "content_type": content_type})
