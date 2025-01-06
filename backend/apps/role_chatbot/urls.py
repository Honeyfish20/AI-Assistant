from django.urls import include, path
from rest_framework import routers
from .views import CheckerViewSet, SkillViewSet, SystemPromptViewSet, RoleChatbotViewSet

router = routers.DefaultRouter()
router.register(r'checker', CheckerViewSet)
router.register(r'skill', SkillViewSet)
router.register(r'role_chatbot', RoleChatbotViewSet)
router.register(r'system_prompts', SystemPromptViewSet)


urlpatterns = [
    path('', include(router.urls)),
]