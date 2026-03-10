"""

Views for Unit → LessonGroup → Lesson → Slide hierarchy.
Import these into views.py with:
    
"""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
import json

from apps.curriculum.models import (
    Unit, LessonGroup, Lesson, LessonSlide,
    SlideWord, SlidePhrase, SlideSentence,
    MultipleChoiceContent, TrueFalseContent,
    FillInBlankContent, BuildBlockContent,
)

from apps.grammar.models import Word, Phrase, Sentence

def is_content_architect(user):
    return user.is_superuser or user.groups.filter(name='ContentArchitect').exists()

architect_required = user_passes_test(is_content_architect, login_url='/cms/login/')

SLIDE_TYPES = [
    ("Intro", "Intro"),
    ("MediaIntro", "Media Intro"),
    ("MultipleChoice", "Multiple Choice"),
    ("TrueFalse", "True / False"),
    ("BuildBlock", "Build Block"),
    ("FillInBlank", "Fill in the Blank"),
    ("MatchPairs", "Match Pairs"),
    ("TypeWord", "Type Word"),
    ("Crossword", "Crossword"),
    ("ToneMarking", "Tone Marking"),
    ("Speaking", "Speaking"),
    ("Sketch", "Sketch"),
    ("TextResponse", "Text Response"),
    ("ReadParagraph", "Read Paragraph"),
]

# Types that have a dedicated content model
CONTENT_MODEL_TYPES = {
    'MultipleChoice': MultipleChoiceContent,
    'TrueFalse': TrueFalseContent,
    'FillInBlank': FillInBlankContent,
    'BuildBlock': BuildBlockContent,
}


# ══════════════════════════════════════════════════════════
#  UNITS
# ══════════════════════════════════════════════════════════

@login_required
@architect_required
def unit_list(request):
    units = Unit.objects.prefetch_related(
        'lesson_groups__lessons'
    ).order_by('title')
    return render(request, 'cms/unit_list.html', {'units': units})


@login_required
@architect_required
def unit_create(request):
    if request.method == 'POST':
        unit = Unit.objects.create(
            title=request.POST['title'],
            description=request.POST.get('description', ''),
        )
        return redirect('cms:unit_detail', pk=unit.pk)
    return render(request, 'cms/unit_form.html', {'action': 'Create'})


@login_required
@architect_required
def unit_detail(request, pk):
    unit = get_object_or_404(
        Unit.objects.prefetch_related('lesson_groups__lessons'),
        pk=pk
    )
    return render(request, 'cms/unit_detail.html', {'unit': unit})


@login_required
@architect_required
def unit_edit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        unit.title = request.POST['title']
        unit.description = request.POST.get('description', '')
        unit.save()
        return redirect('cms:unit_detail', pk=unit.pk)
    return render(request, 'cms/unit_form.html', {'unit': unit, 'action': 'Edit'})


@login_required
@architect_required
@require_POST
def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    unit.delete()
    return redirect('cms:unit_list')


# ══════════════════════════════════════════════════════════
#  LESSON GROUPS
# ══════════════════════════════════════════════════════════

@login_required
@architect_required
def lesson_group_create(request, unit_pk):
    unit = get_object_or_404(Unit, pk=unit_pk)
    if request.method == 'POST':
        # Default order to end of list
        last = unit.lesson_groups.order_by('-order').first()
        order = (last.order + 1) if last else 1.0
        LessonGroup.objects.create(
            unit=unit,
            title=request.POST['title'],
            order=float(request.POST.get('order', order)),
        )
        if request.htmx:
            groups = unit.lesson_groups.prefetch_related('lessons').order_by('order')
            return render(request, 'cms/partials/lesson_group_list.html', {
                'unit': unit, 'groups': groups
            })
        return redirect('cms:unit_detail', pk=unit_pk)

    return render(request, 'cms/partials/lesson_group_form.html', {
        'unit': unit, 'action': 'Create'
    })


@login_required
@architect_required
def lesson_group_edit(request, pk):
    group = get_object_or_404(LessonGroup, pk=pk)
    if request.method == 'POST':
        group.title = request.POST['title']
        group.order = float(request.POST.get('order', group.order))
        group.save()
        if request.htmx:
            groups = group.unit.lesson_groups.prefetch_related('lessons').order_by('order')
            return render(request, 'cms/partials/lesson_group_list.html', {
                'unit': group.unit, 'groups': groups
            })
        return redirect('cms:unit_detail', pk=group.unit_id)
    return render(request, 'cms/partials/lesson_group_form.html', {
        'group': group, 'unit': group.unit, 'action': 'Edit'
    })


@login_required
@architect_required
@require_POST
def lesson_group_delete(request, pk):
    group = get_object_or_404(LessonGroup, pk=pk)
    unit = group.unit
    group.delete()
    if request.htmx:
        groups = unit.lesson_groups.prefetch_related('lessons').order_by('order')
        return render(request, 'cms/partials/lesson_group_list.html', {
            'unit': unit, 'groups': groups
        })
    return redirect('cms:unit_detail', pk=unit.pk)


# ══════════════════════════════════════════════════════════
#  LESSONS
# ══════════════════════════════════════════════════════════

@login_required
@architect_required
def lesson_create(request, group_pk):
    group = get_object_or_404(LessonGroup, pk=group_pk)
    if request.method == 'POST':
        last = group.lessons.order_by('-order').first()
        order = (last.order + 1) if last else 1.0
        lesson = Lesson.objects.create(
            group=group,
            title=request.POST['title'],
            description=request.POST.get('description', ''),
            order=float(request.POST.get('order', order)),
            difficulty=float(request.POST.get('difficulty', 1.0)),
        )
        if request.htmx:
            groups = group.unit.lesson_groups.prefetch_related('lessons').order_by('order')
            return render(request, 'cms/partials/lesson_group_list.html', {
                'unit': group.unit, 'groups': groups
            })
        return redirect('cms:lesson_detail', pk=lesson.pk)
    return render(request, 'cms/partials/lesson_form.html', {
        'group': group, 'action': 'Create'
    })


@login_required
@architect_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(
        Lesson.objects.select_related('group__unit').prefetch_related(
            'slides__slide_words__word',
            'slides__slide_phrases__phrase',
            'slides__slide_sentences__sentence',
        ),
        pk=pk
    )
    return render(request, 'cms/lesson_detail.html', {
        'lesson': lesson,
        'slide_types': SLIDE_TYPES,
    })


@login_required
@architect_required
def lesson_edit(request, pk):
    lesson = get_object_or_404(Lesson.objects.select_related('group__unit'), pk=pk)
    if request.method == 'POST':
        lesson.title = request.POST['title']
        lesson.description = request.POST.get('description', '')
        lesson.order = float(request.POST.get('order', lesson.order))
        lesson.difficulty = float(request.POST.get('difficulty', lesson.difficulty))
        lesson.save()
        return redirect('cms:lesson_detail', pk=lesson.pk)
    return render(request, 'cms/partials/lesson_form.html', {
        'lesson': lesson, 'group': lesson.group, 'action': 'Edit'
    })


@login_required
@architect_required
@require_POST
def lesson_delete(request, pk):
    lesson = get_object_or_404(Lesson.objects.select_related('group__unit'), pk=pk)
    unit = lesson.group.unit
    lesson.delete()
    return redirect('cms:unit_detail', pk=unit.pk)


# ══════════════════════════════════════════════════════════
#  SLIDES
# ══════════════════════════════════════════════════════════

@login_required
@architect_required
def slide_create(request, lesson_pk):
    lesson = get_object_or_404(Lesson.objects.select_related('group__unit'), pk=lesson_pk)
    words    = Word.objects.filter(status='published').order_by('text')
    phrases  = Phrase.objects.filter(status='published').order_by('text')
    sentences = Sentence.objects.filter(status='published').order_by('text')

    if request.method == 'POST':
        with transaction.atomic():
            last = lesson.slides.order_by('-order').first()
            order = (last.order + 1) if last else 1.0
            slide = LessonSlide.objects.create(
                lesson=lesson,
                title=request.POST.get('title', ''),
                slide_type=request.POST['slide_type'],
                order=float(request.POST.get('order', order)),
            )
            _save_slide_content(slide, request.POST)
            _save_slide_relations(slide, request.POST)
        return redirect('cms:lesson_detail', pk=lesson_pk)

    return render(request, 'cms/slide_form.html', {
        'lesson': lesson,
        'slide_types': SLIDE_TYPES,
        'words': words,
        'phrases': phrases,
        'sentences': sentences,
        'action': 'Create',
    })


@login_required
@architect_required
def slide_edit(request, pk):
    slide = get_object_or_404(
        LessonSlide.objects.select_related('lesson__group__unit'),
        pk=pk
    )
    words     = Word.objects.filter(status='published').order_by('text')
    phrases   = Phrase.objects.filter(status='published').order_by('text')
    sentences = Sentence.objects.filter(status='published').order_by('text')

    # Pre-selected IDs for pickers
    selected_word_ids     = list(slide.slide_words.values_list('word_id', flat=True))
    selected_phrase_ids   = list(slide.slide_phrases.values_list('phrase_id', flat=True))
    selected_sentence_ids = list(slide.slide_sentences.values_list('sentence_id', flat=True))

    # Existing content model data
    content_data = _get_content_data(slide)

    if request.method == 'POST':
        with transaction.atomic():
            slide.title      = request.POST.get('title', '')
            slide.slide_type = request.POST['slide_type']
            slide.order      = float(request.POST.get('order', slide.order))
            slide.save()
            # Clear and rebuild content + relations
            _clear_slide_content(slide)
            _save_slide_content(slide, request.POST)
            _save_slide_relations(slide, request.POST)
        return redirect('cms:lesson_detail', pk=slide.lesson_id)

    return render(request, 'cms/slide_form.html', {
        'slide': slide,
        'lesson': slide.lesson,
        'slide_types': SLIDE_TYPES,
        'words': words,
        'phrases': phrases,
        'sentences': sentences,
        'selected_word_ids': selected_word_ids,
        'selected_phrase_ids': selected_phrase_ids,
        'selected_sentence_ids': selected_sentence_ids,
        'content_data': content_data,
        'action': 'Edit',
    })


@login_required
@architect_required
@require_POST
def slide_delete(request, pk):
    slide = get_object_or_404(LessonSlide, pk=pk)
    lesson_pk = slide.lesson_id
    slide.delete()
    if request.htmx:
        lesson = get_object_or_404(Lesson, pk=lesson_pk)
        return render(request, 'cms/partials/slide_list.html', {
            'lesson': lesson,
            'slides': lesson.slides.order_by('order'),
            'slide_types': SLIDE_TYPES,
        })
    return redirect('cms:lesson_detail', pk=lesson_pk)


@login_required
@architect_required
@require_POST
def slide_reorder(request, pk):
    """HTMX endpoint: update slide order via drag-and-drop."""
    slide = get_object_or_404(LessonSlide, pk=pk)
    new_order = request.POST.get('order')
    if new_order:
        slide.order = float(new_order)
        slide.save(update_fields=['order'])
    return HttpResponse(status=204)


@login_required
@architect_required
def slide_content_panel(request):
    """
    HTMX endpoint: returns the dynamic content panel for a given slide_type.
    Called when the slide_type select changes in the slide form.
    """
    slide_type = request.GET.get('slide_type', '')
    slide_pk   = request.GET.get('slide_pk')
    slide      = LessonSlide.objects.filter(pk=slide_pk).first() if slide_pk else None
    content_data = _get_content_data(slide) if slide else {}

    sentences = Sentence.objects.filter(status='published').order_by('text')

    return render(request, 'cms/partials/slide_content_panel.html', {
        'slide_type': slide_type,
        'slide': slide,
        'content_data': content_data,
        'sentences': sentences,
    })


# ══════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════

def _save_slide_relations(slide, post_data):
    """Save SlideWord, SlidePhrase, SlideSentence from POST data."""
    SlideWord.objects.filter(slide=slide).delete()
    SlidePhrase.objects.filter(slide=slide).delete()
    SlideSentence.objects.filter(slide=slide).delete()

    for i, word_id in enumerate(post_data.getlist('word_ids')):
        SlideWord.objects.create(slide=slide, word_id=word_id, order=float(i))

    for i, phrase_id in enumerate(post_data.getlist('phrase_ids')):
        SlidePhrase.objects.create(slide=slide, phrase_id=phrase_id, order=float(i))

    for i, sentence_id in enumerate(post_data.getlist('sentence_ids')):
        SlideSentence.objects.create(slide=slide, sentence_id=sentence_id, order=float(i))


def _save_slide_content(slide, post_data):
    """Save the type-specific content model if applicable."""
    t = slide.slide_type

    if t == 'MultipleChoice':
        options = _parse_mc_options(post_data)
        MultipleChoiceContent.objects.update_or_create(
            slide=slide,
            defaults={
                'question': post_data.get('mc_question', ''),
                'options': options,
            }
        )

    elif t == 'TrueFalse':
        options = _parse_mc_options(post_data)
        TrueFalseContent.objects.update_or_create(
            slide=slide,
            defaults={
                'question': post_data.get('tf_question', ''),
                'options': options,
            }
        )

    elif t == 'FillInBlank':
        blanks = _parse_blanks(post_data)
        sentence_id = post_data.get('fib_sentence_id')
        if sentence_id:
            FillInBlankContent.objects.update_or_create(
                slide=slide,
                defaults={
                    'sentence_id': sentence_id,
                    'blanks': blanks,
                }
            )

    elif t == 'BuildBlock':
        word_order = post_data.get('bb_word_order')
        sentence_id = post_data.get('bb_sentence_id')
        if sentence_id:
            BuildBlockContent.objects.update_or_create(
                slide=slide,
                defaults={
                    'sentence_id': sentence_id,
                    'word_order': json.loads(word_order) if word_order else None,
                }
            )


def _clear_slide_content(slide):
    """Remove old content model when slide_type may have changed."""
    for Model in CONTENT_MODEL_TYPES.values():
        Model.objects.filter(slide=slide).delete()


def _get_content_data(slide):
    """Return existing content model data as a flat dict for template pre-population."""
    if not slide:
        return {}
    t = slide.slide_type
    data = {}

    if t == 'MultipleChoice' and hasattr(slide, 'mc_content'):
        data['mc_question'] = slide.mc_content.question
        data['mc_options']  = slide.mc_content.options

    elif t == 'TrueFalse' and hasattr(slide, 'tf_content'):
        data['tf_question'] = slide.tf_content.question
        data['tf_options']  = slide.tf_content.options

    elif t == 'FillInBlank' and hasattr(slide, 'fib_content'):
        data['fib_sentence_id'] = slide.fib_content.sentence_id
        data['fib_blanks']      = slide.fib_content.blanks

    elif t == 'BuildBlock' and hasattr(slide, 'bb_content'):
        data['bb_sentence_id'] = slide.bb_content.sentence_id
        data['bb_word_order']  = slide.bb_content.word_order

    return data


def _parse_mc_options(post_data):
    """
    Expects POST fields: option_text_0, option_correct_0, option_text_1 ...
    Returns: [{"text": "...", "is_correct": True}, ...]
    """
    options = []
    i = 0
    while f'option_text_{i}' in post_data:
        options.append({
            'text': post_data.get(f'option_text_{i}', ''),
            'is_correct': f'option_correct_{i}' in post_data,
        })
        i += 1
    return options


def _parse_blanks(post_data):
    """
    Expects POST fields: blank_start_0, blank_end_0, blank_start_1 ...
    Returns: [{"start": 10, "end": 14}, ...]
    """
    blanks = []
    i = 0
    while f'blank_start_{i}' in post_data:
        try:
            blanks.append({
                'start': int(post_data[f'blank_start_{i}']),
                'end':   int(post_data[f'blank_end_{i}']),
            })
        except (ValueError, KeyError):
            pass
        i += 1
    return blanks
