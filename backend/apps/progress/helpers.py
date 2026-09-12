from django.utils import timezone
from django.db.models import F

"""
Post.objects.filter(id=post_id).update(
    views=F("views") + 1
)
"""
def update_progress(progress_item, quality: int):
    """
    quality: 0-5
      0-2 = failed (show again soon)
      3   = passed with difficulty
      4   = passed
      5   = passed easily
    """
    if quality < 3:
        # Failed — reset repetitions, show again in 1 day
        progress_item.repetitions = 0
        progress_item.interval    = 1
    else:
        if progress_item.repetitions == 0:
            progress_item.interval = 1
        elif progress_item.repetitions == 1:
            progress_item.interval = 6
        else:
            progress_item.interval = round(progress_item.interval * progress_item.ease_factor)

        progress_item.repetitions += 1

    # Update ease factor — gets harder to shift as repetitions increase
    progress_item.ease_factor = max(
        1.3,
        progress_item.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    )

    progress_item.last_reviewed = timezone.now()
    progress_item.next_review   = timezone.now() + timezone.timedelta(days=progress_item.interval)
    progress_item.save()
