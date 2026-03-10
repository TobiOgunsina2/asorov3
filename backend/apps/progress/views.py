from django.shortcuts import render
from .const import max_idiom_items
# Create your views here.
"""
due_words = UserWordProgress.objects.filter(
    user=user,
    due__lte=now()
).order_by("due")[:max_review_items]

due_idioms = UserPhraseProgress.objects.filter(
    user=user,
    due__lte=now()
).order_by("due")[:max_idiom_items]
"""