from django.db import models
from django.contrib.auth import get_user_model
from assistant_settings.models import BaseModel

import json
# Create your models here.

class UserPrompt(models.Model):
    id = models.AutoField(primary_key=True)
    system_prompt = models.TextField()
    preset_user_message = models.TextField(help_text="Only for the first round", null=True, blank=True)
    preset_assistant_message = models.TextField(help_text="Only for the first round", null=True, blank=True)
    description = models.TextField(default="")
    create_time = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='user_prompt')
    note = models.TextField()
    model_id = models.ForeignKey(BaseModel, on_delete=models.CASCADE)
    max_tokens = models.IntegerField(default=8192)
    stop_sequences = models.TextField(blank=True, null=True)
    temperature = models.FloatField(default=0)
    
    class Mate:
        verbose_name = "User Prompts"
        verbose_name_plural = "User Prompts"
        app_label = "general_assistant"
    
    def __str__(self):
        return str(self.id)