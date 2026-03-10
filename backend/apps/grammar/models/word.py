from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from apps.language_cms.models import CMSContentMixin

# These are the generic parts of speech which a word can have
PART_OF_SPEECH_CHOICES = [
    ('noun', 'Noun'),
    ('verb', 'Verb'),
    ('adjective', 'Adjective'),
    ('adverb', 'Adverb'),
    ('pronoun', 'Pronoun'),
    ('preposition', 'Preposition'),
    ('particle', 'Particle'),
    ('conjunction', 'Conjunction'),
    ('interjection', 'Interjection'),
    ('question', 'Question'),
]

# Content Mixin adds:
#   draft
#   review
#   published status, 
#   creator tracking, 
#   and internal notes. 

class Word(CMSContentMixin, models.Model):
    text = models.CharField(max_length=100)
    translation = models.CharField(max_length=255)
    part_of_speech = models.CharField(max_length=50, choices=PART_OF_SPEECH_CHOICES, null=True, blank=True)
    # media = GenericRelation(Media)

    # related words help with multiple choice slide generation as they can be picked from to 
    # offer alternative options
    related_words = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.text

