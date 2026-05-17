from django.db import models
from apps.courses.constants import LESSON_ID_LENGTH
from apps.courses.models.Unit import Unit
from apps.courses.utils import generate_unique_short_code
from django.db import IntegrityError, transaction


# Having lesson group allows concepts to be split up into multiple parts without
# taking up lot's of screen real estate on the front end. Makes lessons more digestable
class LessonGroup(models.Model):
    """
    Optional grouping of lessons inside a unit.
    Example:
    - "Grammar Basics"
    - "Final Project"
    - "Part 1 + Part 2"
    """

    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lesson_groups")
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    def __str__(self):
        return str("Lesson Group - " + self.title)


class Lesson(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="lessons")

    group = models.ForeignKey(LessonGroup, null=True, blank=True, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=LESSON_ID_LENGTH, unique=True, editable=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()

    difficulty = models.IntegerField(default=1)  # New field to indicate lesson difficulty

    def __str__(self):
        return str("Lesson - " + self.title)
    
    # Override save method to generate unique short code for the lesson
    def save(self, *args, **kwargs):
        if self.short_code:
            return super().save(*args, **kwargs)

        while True:
            try:
                self.short_code = generate_unique_short_code(Lesson)

                with transaction.atomic():
                    return super().save(*args, **kwargs)

            except IntegrityError:
                # Collision occurred, retry
                self.short_code = None
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["unit", "group", "order"],
                name="unique_lesson_order"
            )
        ]
