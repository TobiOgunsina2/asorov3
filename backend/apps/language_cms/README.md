# LinguaForge CMS — Integration Guide

A bespoke, HTMX-powered Content Management System for language course architects.
Provides Create / Edit / Delete / Search / Publish workflow for **Words**, **Phrases**, and **Sentences** — and nothing else.

---

## Directory Structure

```
language_cms/
├── __init__.py
├── apps.py
├── admin.py               # intentionally empty
├── models.py              # CMSStatusMixin — add to your existing models
├── views.py               # all CMS views
├── urls.py                # URL config
├── management/
│   └── commands/
│       └── setup_cms_group.py
└── templates/
    └── cms/
        ├── base.html
        ├── dashboard.html
        ├── word_list.html
        ├── word_form.html
        ├── phrase_list.html
        ├── phrase_form.html
        ├── sentence_list.html
        ├── sentence_form.html
        └── partials/
            ├── word_table.html
            ├── phrase_table.html
            ├── sentence_table.html
            ├── preview_word.html
            ├── preview_phrase.html
            ├── preview_sentence.html
            └── status_badge.html
```

---

## Step 1 — Add fields to your existing models

The CMS requires `status`, `published_at`, `created_at`, and `updated_at` fields on `Word`, `Phrase`, and `Sentence`.

Add `CMSStatusMixin` to each:

```python
# your_app/models.py
from language_cms.models import CMSStatusMixin

class Word(CMSStatusMixin, models.Model):
    text = models.CharField(max_length=100)
    translation = models.CharField(max_length=255)
    part_of_speech = models.CharField(max_length=50)

class Phrase(CMSStatusMixin, models.Model):
    # ... existing fields

class Sentence(CMSStatusMixin, models.Model):
    # ... existing fields
```

Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 2 — Install the app

```python
# settings.py
INSTALLED_APPS = [
    ...
    'language_cms',
]
```

---

## Step 3 — Wire up URLs

```python
# your_project/urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cms/', include('language_cms.urls', namespace='cms')),
    path('accounts/', include('django.contrib.auth.urls')),  # for login/logout
]
```

---

## Step 4 — Fix the model import in views.py

Open `language_cms/views.py` and update line 14:

```python
# Change this:
from your_app.models import (...)

# To your actual app name, e.g.:
from courses.models import Word, Phrase, PhraseWord, Sentence, SentenceComponent, PART_OF_SPEECH_CHOICES
```

---

## Step 5 — Create the ContentArchitect group

```bash
python manage.py setup_cms_group
```

Then assign users to this group via Django Admin or the shell:

```python
from django.contrib.auth.models import User, Group
user = User.objects.get(username='alice')
group = Group.objects.get(name='ContentArchitect')
user.groups.add(group)
```

> ContentArchitect users should NOT have `is_staff=True` — they won't see Django Admin.

---

## Step 6 — Template filter for JSON

The sentence form uses `|tojson` filter. Register it in your app or add to a templatetags file:

```python
# your_app/templatetags/json_extras.py
import json
from django import template

register = template.Library()

@register.filter
def tojson(value):
    return json.dumps(value)
```

And load it in `sentence_form.html` if not already auto-loaded:
```
{% load json_extras %}
```

---

## Step 7 — Login redirect

Ensure `LOGIN_URL` is set in settings so unauthenticated users are redirected:

```python
# settings.py
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/cms/'
```

---

## Features Overview

| Feature | Details |
|---|---|
| **Dashboard** | Live counts of words/phrases/sentences by status, recent items |
| **Word CRUD** | Text, translation, part-of-speech (all 10 types), status |
| **Phrase CRUD** | Text, translation + draggable ordered word picker (PhraseWord through model) |
| **Sentence CRUD** | Text, translation + dynamic component builder (Word or Phrase, with highlight offsets) |
| **Search** | HTMX live search on text + translation, debounced 300ms |
| **Filter** | By part-of-speech (words), by status (all types) |
| **Publish workflow** | Draft / Published toggle, sets `published_at` timestamp |
| **Preview modal** | HTMX-loaded preview of any item without leaving the list |
| **Confirm delete** | Browser confirm dialog before destructive actions |
| **Access control** | `ContentArchitect` group gate, redirects to login |

---

## Design System

The CMS uses a clean editorial style with:
- **Syne** (display font, headings) + **DM Sans** (body)
- Ink/paper neutral palette with jade green accents
- CSS custom properties for easy theming
- No external CSS framework dependencies
