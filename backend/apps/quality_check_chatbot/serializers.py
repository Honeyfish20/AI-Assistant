from rest_framework import serializers
from .models import DialogueChecker, QualityCheckChatbot, KnowledgeBaseDialogueChecker


class DialogueCheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialogueChecker
        fields = '__all__'

class KnowledgeBaseDialogueCheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBaseDialogueChecker
        fields = '__all__'

class QualityCheckChatbotSerializer(serializers.ModelSerializer):
    dialogue_checkers = DialogueCheckerSerializer(many=True, read_only=True)
    knowledge_base_dialogue_checkers = KnowledgeBaseDialogueCheckerSerializer(many=True, read_only=True)

    class Meta:
        model = QualityCheckChatbot
        fields = '__all__'