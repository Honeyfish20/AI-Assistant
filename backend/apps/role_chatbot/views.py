from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Checker, Skill, RoleChatbot, SystemPrompt
from .serializers import CheckerSerializer, SkillSerializer, SystemPromptSerializer , RoleChatbotSerializer

class CheckerViewSet(viewsets.ModelViewSet):
    queryset = Checker.objects.all()
    serializer_class = CheckerSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class RoleChatbotViewSet(viewsets.ModelViewSet):
    queryset = RoleChatbot.objects.all()
    serializer_class = RoleChatbotSerializer
    

class SystemPromptViewSet(viewsets.ModelViewSet):
    queryset = SystemPrompt.objects.all()
    serializer_class = SystemPromptSerializer