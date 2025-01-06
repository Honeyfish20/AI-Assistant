from django.db import models
from assistant_settings.models import BaseModel

class DialogueChecker(models.Model):
    id = models.AutoField(primary_key=True)
    dialogue_checker_name = models.CharField(max_length=100)
    dialogue_checker_description = models.TextField()
    dialogue_checker_prompt = models.TextField()
    model_id = models.ForeignKey(BaseModel, on_delete=models.CASCADE)
    max_tokens = models.IntegerField(default=8192)
    stop_sequences = models.TextField(blank=True, null=True)
    temperature = models.FloatField(default=0)
    is_knowledge_base = models.BooleanField(default=False)

    def __str__(self):
        return self.dialogue_checker_name
    

class KnowledgeBaseDialogueChecker(models.Model):
    id = models.AutoField(primary_key=True)
    knowledge_base_dialogue_checker_name = models.CharField(max_length=100)
    knowledge_base_dialogue_checker_description = models.TextField()
    knowledge_base_dialogue_checker_prompt = models.TextField()
    query_list_generation_prompt = models.TextField(help_text="query list generation prompt is used for generating key-words or key-sentences to retrieval related information in vector databse, please let it output a list.")
    model_id = models.ForeignKey(BaseModel, on_delete=models.CASCADE)
    max_tokens = models.IntegerField(default=8192)
    stop_sequences = models.TextField(blank=True, null=True)
    temperature = models.FloatField(default=0)
    knowledge_base_id = models.TextField(default="", help_text="Now, only support the bedrock knowledge base. Please make sure you can access the knowledge base in your environment.")

    def __str__(self):
        return self.knowledge_base_dialogue_checker_name
    

class QualityCheckChatbot(models.Model):
    id = models.AutoField(primary_key=True)
    qc_chat_name = models.CharField(max_length=100)
    qc_chat_background = models.TextField()
    dialogue_checkers = models.ManyToManyField(DialogueChecker, related_name='quality_check_chatbots', blank=True, null=True)
    knowledge_base_dialogue_checkers = models.ManyToManyField(KnowledgeBaseDialogueChecker, related_name='knowledge_base_quality_check_chatbots', blank=True, null=True)

    def __str__(self):
        return self.qc_chat_name
    