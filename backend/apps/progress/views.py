from django.shortcuts import render
from .constants import max_idiom_items
from django.utils import timezone


# Create your views here.

def update_progress(progress, quality: int):
    """
    quality: 0-5
      0-2 = failed (show again soon)
      3   = passed with difficulty
      4   = passed
      5   = passed easily
    """
    if quality < 3:
        # Failed — reset repetitions, show again in 1 day
        progress.repetitions = 0
        progress.interval    = 1
    else:
        if progress.repetitions == 0:
            progress.interval = 1
        elif progress.repetitions == 1:
            progress.interval = 6
        else:
            progress.interval = round(progress.interval * progress.ease_factor)

        progress.repetitions += 1

    # Update ease factor — gets harder to shift as repetitions increase
    progress.ease_factor = max(
        1.3,
        progress.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    )

    progress.last_reviewed = timezone.now()
    progress.next_review   = timezone.now() + timezone.timedelta(days=progress.interval)
    progress.save()
