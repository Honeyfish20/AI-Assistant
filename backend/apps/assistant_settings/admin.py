from django.contrib import admin
from .models import BaseModel

@admin.register(BaseModel)
class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('model_id', 'max_tokens', 'stop_sequences', 'temperature')
    list_filter = ('model_id',)
    search_fields = ('model_id',)
