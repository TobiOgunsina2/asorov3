from django.db import models

class RoleName(models.TextChoices):
    LEARNER         = 'learner',         'Learner'
    CONTENT_CREATOR = 'content_creator', 'Content Creator'
    REVIEWER        = 'reviewer',        'Reviewer'
    #MODERATOR       = 'moderator',       'Moderator'