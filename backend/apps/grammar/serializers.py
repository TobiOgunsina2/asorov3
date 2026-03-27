from rest_framework import serializers
from apps.grammar.models.sentence import Sentence

from apps.grammar.models.sentence import Sentence, SentenceComponent
from apps.grammar.models.phrase import Phrase
from apps.grammar.models.word import Word



class RelatedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ["id", "text", "translation"]  # omit 'related_words' here

class WordSerializer(serializers.ModelSerializer):
    related_words = RelatedWordSerializer(many=True, read_only=True)

    class Meta:
        model = Word
        fields = [
            "id", "text", "translation", "related_words",
        ]

class PhraseSerializer(serializers.ModelSerializer):
    phrase_words = RelatedWordSerializer(many=True, read_only=True)
      
    class Meta:
        model = Phrase
        fields = [
            "id", "text", "translation", "difficulty",
            "is_idiom", "phrase_words"
        ]

class SentencePhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phrase
        fields = [
            "id", "text", "translation", "difficulty",
            "is_idiom"
        ]

class SentenceComponentSerializer(serializers.ModelSerializer):
    component_type = serializers.SerializerMethodField()
    component = serializers.SerializerMethodField()

    class Meta:
        model = SentenceComponent
        fields = [
            "id", "order",
            "highlight_start", "highlight_end",
            "component_type", "component",
        ]

    def get_component_type(self, obj):
        if obj.word_id:
            return "word"
        if obj.phrase_id:
            return "phrase"
        return None

    def get_component(self, obj):
        if obj.word_id:
            return RelatedWordSerializer(obj.word).data
        if obj.phrase_id:
            return SentencePhraseSerializer(obj.phrase, context=self.context).data
        return None


class SentenceSerializer(serializers.ModelSerializer):
    components = SentenceComponentSerializer(many=True, read_only=True)

    class Meta:
        model = Sentence
        fields = [
            "id", "text", "translation", "difficulty",
            "components",
        ]