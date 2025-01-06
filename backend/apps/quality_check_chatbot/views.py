from rest_framework import viewsets
from .models import DialogueChecker, QualityCheckChatbot, KnowledgeBaseDialogueChecker
from .serializers import DialogueCheckerSerializer, QualityCheckChatbotSerializer, KnowledgeBaseDialogueCheckerSerializer

class DialogueCheckerViewSet(viewsets.ModelViewSet):
    queryset = DialogueChecker.objects.all()
    serializer_class = DialogueCheckerSerializer
    
class KnowledgeBaseDialogueCheckerViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeBaseDialogueChecker.objects.all()
    serializer_class = KnowledgeBaseDialogueCheckerSerializer
    
class QualityCheckChatbotViewSet(viewsets.ModelViewSet):
    queryset = QualityCheckChatbot.objects.all()
    serializer_class = QualityCheckChatbotSerializer