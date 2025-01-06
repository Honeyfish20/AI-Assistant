from django.contrib import admin
from .models import Checker, Skill, RoleChatbot, SystemPrompt

# Register your models here.

admin.site.site_header = 'GenAIIC Smart Training Assistant'
admin.site.site_title = 'GenAIIC Smart Training Assistant'
admin.site.index_title = 'GenAIIC Smart Training Assistant'


@admin.register(Checker)
class CheckerAdmin(admin.ModelAdmin):
    list_display = ('id', 'checker_name', 'checker_description', 'checker_prompt', 'checker_time_limit', 'model_id', 'max_tokens', 'temperature')
    list_filter = ('model_id',)
    search_fields = ('checker_name', 'checker_description', 'checker_prompt')
    
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'skill_name', 'skill_description', 'skill_examples', 'model_id', 'max_tokens', 'temperature')
    list_filter = ('model_id',)
    search_fields = ('skill_name', 'skill_description', 'skill_examples')
    filter_horizontal = ('skill_checkers',)
    
@admin.register(RoleChatbot)
class RoleChatbotAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_name', 'role_background', 'chat_background', 'language_styles', 'system_prompt')
    search_fields = ('role_name', 'role_background', 'chat_background')
    filter_horizontal = ('skills',)
    
@admin.register(SystemPrompt)
class SystemPromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'prompt', 'create_time', 'creator')
    list_filter = ('id',)
    search_fields = ('id',)
    