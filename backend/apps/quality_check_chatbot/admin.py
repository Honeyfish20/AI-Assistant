from django.contrib import admin
from .models import DialogueChecker, QualityCheckChatbot, KnowledgeBaseDialogueChecker

@admin.register(DialogueChecker)
class DialogueCheckerAdmin(admin.ModelAdmin):
    list_display = ('id', 'dialogue_checker_name', 'dialogue_checker_description', 'model_id', 'max_tokens', 'stop_sequences', 'temperature')
    list_filter = ('model_id',)
    search_fields = ('dialogue_checker_name', 'dialogue_checker_description')
    
@admin.register(KnowledgeBaseDialogueChecker)
class KnowledgeBaseDialogueCheckerAdmin(admin.ModelAdmin):
    list_display = ('id', 'knowledge_base_dialogue_checker_name', 'knowledge_base_dialogue_checker_description')
    list_filter = ('model_id',)
    search_fields = ('knowledge_base_dialogue_checker_name', 'knowledge_base_dialogue_checker_description', 'knowledge_base_dialogue_checker_prompt')

    
@admin.register(QualityCheckChatbot)
class QualityCheckChatbotAdmin(admin.ModelAdmin):
    list_display = ('qc_chat_name', 'qc_chat_background')
    filter_horizontal = ('dialogue_checkers', 'knowledge_base_dialogue_checkers', )