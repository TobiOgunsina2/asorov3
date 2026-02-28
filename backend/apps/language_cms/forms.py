# language_cms/forms.py
from django import forms
from django.forms import inlineformset_factory

# ── Import from your actual app, e.g. "from courses.models import ..."
# We use string references here so this file is portable.
# Replace the imports below with your real model imports.
#


from apps.grammar.models.word import PART_OF_SPEECH_CHOICES

PART_OF_SPEECH_CHOICES = [
    ('noun', 'Noun'), ('verb', 'Verb'), ('adjective', 'Adjective'),
    ('adverb', 'Adverb'), ('pronoun', 'Pronoun'), ('preposition', 'Preposition'),
    ('particle', 'Particle'), ('conjunction', 'Conjunction'),
    ('interjection', 'Interjection'), ('question', 'Question'),
]

STATUS_CHOICES = [('draft', 'Draft'), ('review', 'In Review'), ('published', 'Published')]


class WordForm(forms.Form):
    text = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'cms-input', 'placeholder': 'Word in target language'}))
    translation = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'cms-input', 'placeholder': 'English translation'}))
    part_of_speech = forms.ChoiceField(choices=PART_OF_SPEECH_CHOICES, widget=forms.Select(attrs={'class': 'cms-select'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'cms-textarea', 'rows': 2, 'placeholder': 'Internal notes...'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'cms-select'}))


class PhraseForm(forms.Form):
    text = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'cms-input', 'placeholder': 'Phrase in target language'}))
    translation = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'cms-input', 'placeholder': 'English translation'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'cms-textarea', 'rows': 2, 'placeholder': 'Internal notes...'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'cms-select'}))
    # Word IDs for the M2M — handled in view
    word_ids = forms.CharField(required=False, widget=forms.HiddenInput())


class SentenceForm(forms.Form):
    text = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'cms-input', 'placeholder': 'Sentence in target language'}))
    translation = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'cms-input', 'placeholder': 'English translation'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'cms-textarea', 'rows': 2, 'placeholder': 'Internal notes...'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'cms-select'}))


class SearchFilterForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'cms-input search-input', 'placeholder': 'Search...', 'hx-get': '', 'hx-trigger': 'keyup changed delay:300ms', 'hx-target': '#content-list', 'hx-push-url': 'true'}))
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'cms-select', 'hx-get': '', 'hx-trigger': 'change', 'hx-target': '#content-list', 'hx-include': '[name=q]'})
    )
    pos = forms.ChoiceField(
        required=False,
        choices=[('', 'All Parts of Speech')] + PART_OF_SPEECH_CHOICES,
        widget=forms.Select(attrs={'class': 'cms-select', 'hx-get': '', 'hx-trigger': 'change', 'hx-target': '#content-list', 'hx-include': '[name=q],[name=status]'})
    )
