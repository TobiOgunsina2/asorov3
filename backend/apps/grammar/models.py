from django.db import models

# Create your models here.

"""
These models give structure for words, phrases and sentences. The grammatical foundation of the language
Each model contains a text field to allow for input of specifc spelling, accounting for tone and elision
English translation is also provided
They then connect to other related grammatical models to allow users to form intuition and recognize roots of phrases and sentences 

The model design here allows for progress tracking of words and phrases through sentences

"""