from django.contrib import admin
from .models import UserPrompt

@admin.register(UserPrompt)
class UserPromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'system_prompt', 'creator', 'create_time', 'model_id', 'max_tokens', 'temperature')
    search_fields = ('system_prompt', 'creator__username')
    list_filter = ('creator', 'create_time', 'model_id')