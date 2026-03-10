from apps.grammar.models.sentence import Sentence, SentenceComponent, SentenceWordIndex
from apps.grammar.models.phrase import Phrase
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

# Signals to maintain the SentenceWordIndex for efficient querying of sentences by words.
@receiver(post_save, sender=SentenceComponent)
def update_sentence_index(sender, instance, **kwargs):
    rebuild_sentence_index(instance.sentence)

def rebuild_sentence_index(sentence):
    words = set()

    components = sentence.components.select_related(
        "word", "phrase"
    ).prefetch_related("phrase__words")

    for comp in components:
        if comp.word:
            words.add(comp.word)

        if comp.phrase:
            words.update(comp.phrase.words.all())

    SentenceWordIndex.objects.filter(sentence=sentence).delete()

    SentenceWordIndex.objects.bulk_create(
        [
            SentenceWordIndex(sentence=sentence, word=w)
            for w in words
        ]
    )
# Whenever a Phrase's words are changed, we need to update the index for sentences that include that phrase.
@receiver(m2m_changed, sender=Phrase.words.through)
def phrase_words_changed(sender, instance, **kwargs):
    sentences = Sentence.objects.filter(
        components__phrase=instance
    ).distinct()

    for sentence in sentences:
        rebuild_sentence_index(sentence)
