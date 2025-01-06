from django.urls import path, include
from rest_framework import routers
from .views import UserPromptViewSet, ChatFeishuView

router = routers.DefaultRouter()
router.register(r'user_prompts', UserPromptViewSet)
# router.register(r'chat_feishu', ChatFeishuView.as_view(), name='chat_feishu')

urlpatterns = [
    # 其他URL模式
    path('', include(router.urls)),
    path('chat_feishu', ChatFeishuView.as_view(), name='chat_feishu')
]