# language_cms/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings

class PublishStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    REVIEW = "review", "In Review"
    PUBLISHED = "published", "Published"


class CMSContentMixin(models.Model):
    """
    Abstract mixin — add to Word, Phrase, Sentence models:
        class Word(CMSContentMixin, models.Model): ...
    """
    status = models.CharField(
        max_length=20,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
        db_index=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, help_text="Internal notes (not shown to learners)")

    class Meta:
        abstract = True
