from progress.models import UserWordProgress

## Get full lesson payload

def build_lesson_payload(user, lesson_code):
    lesson = get_lesson_with_content(lesson_code)

    review_data = get_lesson_review_data(user)

    return (lesson, review_data)


## Get Lesson from Lesson Code

from django.db.models import Prefetch
from models.slide import LessonSlide
from models.lesson import Lesson

def get_lesson_with_content(lesson_code):
    slide_queryset = LessonSlide.objects.with_slide_content()

    lesson = (
        Lesson.objects
        .prefetch_related(
            Prefetch("slides", queryset=slide_queryset)
        )
        .get(code=lesson_code)
    )

    return lesson


"""----------------------------------------------------------------------------------------------------------------------------"""

from constants import max_lesson_review_items, max_practice_review_items
from django.utils import timezone

## Get review slides | Words and associated Sentence


def _get_review_data(user, review_item_count=max_lesson_review_items):
    due_words = UserWordProgress.objects.filter(
            user=user,
            due__lte=timezone.now()
    ).select_related("word")[:review_item_count]

    words = [dw.word for dw in due_words]
    review_data = get_sentences_for_words(words, user.difficulty)
    
    return review_data

# Get review data for lesson and practice sections separately to allow different review item counts

def get_lesson_review_data(user):
    review_data = _get_review_data(user, max_lesson_review_items)
    return review_data

def get_practice_review_data(user):
    review_data = _get_review_data(user, max_practice_review_items)
    return review_data

from apps.grammar.models import Sentence
from collections import defaultdict
import random

## Helper for getting sentence for review words

def get_sentences_for_words(words: list, difficulty: int) -> list[dict]:
    """
    Returns a mapping of word -> random Sentence for a batch of words.
    Sentences are filtered by difficulty and randomized in Python.
    """

    word_ids = [word.id for word in words]

    candidate_sentences = (
        Sentence.objects
        .filter(
            components__word_id__in=word_ids,
            difficulty__lte=difficulty,
        )
        .prefetch_related('components__word')
    )

    sentences_by_word = defaultdict(list)
    for sentence in candidate_sentences:
        for component in sentence.components.all():
            if component.word_id in word_ids:
                sentences_by_word[component.word_id].append(sentence)
    
    word_lookup = {word.id: word for word in words}

    return [
        {"word": word_lookup[word_id], "sentence": random.choice(sentences), "type": "review"}
        for word_id, sentences in sentences_by_word.items()
    ]

"""

from django.db import transaction


@transaction.atomic
def enroll_user_in_course(*, user, course):

    if course.is_archived:
        raise CourseArchived()

    enrollment, created = Enrollment.objects.get_or_create(
        user=user,
        course=course
    )

    if created:
        send_enrollment_email.delay(user.id)

    return enrollment
    """
