from apps.grammar.models import Sentence
from collections import defaultdict
import random


def get_sentences_for_words(words: list, difficulty: int) -> list[dict]:
    """
    Returns a mapping of word -> random Sentence for a batch of words.
    Sentences are filtered by difficulty and randomized in Python.
    """

    word_ids = [word.id for word in words]

    candidate_sentences = (
        Sentence.objects
        .filter(
            components__word_id__in=word_ids,
            difficulty__lte=difficulty,
        )
        .prefetch_related('components__word', 'components__phrase')
    )

    sentences_by_word = defaultdict(list)
    for sentence in candidate_sentences:
        for component in sentence.components.all():
            if component.word_id in word_ids:
                sentences_by_word[component.word_id].append(sentence)
    
    word_lookup = {word.id: word for word in words}


    return [
        {"word": word_lookup[word_id], "sentence": random.choice(sentences), "type": "review"}
        for word_id, sentences in sentences_by_word.items()
    ]