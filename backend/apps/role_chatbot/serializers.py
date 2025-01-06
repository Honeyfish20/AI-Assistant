from rest_framework import serializers
from .models import Checker, Skill, RoleChatbot, SystemPrompt

class CheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checker
        fields = '__all__'
        

class SkillSerializer(serializers.ModelSerializer):
    skill_checkers = CheckerSerializer(many=True, read_only=True)

    class Meta:
        model = Skill
        fields = '__all__'
        
class SystemPromptSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = SystemPrompt
        fields = '__all__'
        
class RoleChatbotSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    system_prompt = SystemPromptSerializer(read_only=True)
    class Meta:
        model = RoleChatbot
        fields = '__all__'
    
