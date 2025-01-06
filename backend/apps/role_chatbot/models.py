from django.db import models
from assistant_settings.models import BaseModel
from django.contrib.auth import get_user_model


class Checker(models.Model):
    id = models.AutoField(primary_key=True)
    checker_name = models.CharField(max_length=255)
    checker_description = models.TextField()
    checker_prompt = models.TextField()
    checker_time_limit = models.IntegerField()
    model_id = models.ForeignKey(BaseModel, on_delete=models.CASCADE)
    max_tokens = models.IntegerField(default=8192)
    stop_sequences = models.TextField(blank=True, null=True)
    temperature = models.FloatField(default=0)

    def __str__(self):
        return self.checker_name
    

class Skill(models.Model):
    id = models.AutoField(primary_key=True)
    skill_name = models.CharField(max_length=255)
    skill_description = models.TextField()
    skill_examples = models.TextField(blank=True, null=True)
    skill_checkers = models.ManyToManyField('Checker', related_name='skill_checkers', blank=True, null=True)
    model_id = models.ForeignKey(BaseModel, on_delete=models.CASCADE)
    max_tokens = models.IntegerField(default=8192)
    stop_sequences = models.TextField(blank=True, null=True)
    temperature = models.FloatField(default=0)

    def __str__(self):
        return self.skill_name
    
class SystemPrompt(models.Model):
    id = models.AutoField(primary_key=True)
    prompt = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='core_prompts')
    
    def __str__(self):
        return str(self.id)
    
    class Mate:
        verbose_name = "System Prompt"
        verbose_name_plural = "System Prompts"

class RoleChatbot(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100)
    role_background = models.TextField()
    chat_background = models.TextField()
    language_styles = models.TextField()
    skills = models.ManyToManyField('Skill', related_name='role_chat_bot_skills')
    system_prompt = models.ForeignKey(SystemPrompt, on_delete=models.CASCADE, related_name='role_chat_bot_system_prompt')


    def __str__(self):
        return self.role_name
    
