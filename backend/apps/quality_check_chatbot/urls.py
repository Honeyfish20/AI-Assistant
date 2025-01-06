from django.urls import include, path
from rest_framework import routers
from .views import DialogueCheckerViewSet, QualityCheckChatbotViewSet, KnowledgeBaseDialogueCheckerViewSet

router = routers.DefaultRouter()
router.register(r'dialogue_checkers', DialogueCheckerViewSet)
router.register(r'knowledge_base_dialogue_checkers', KnowledgeBaseDialogueCheckerViewSet)
router.register(r'quality_check_chatbots', QualityCheckChatbotViewSet)


urlpatterns = [
    path('', include(router.urls)),
]