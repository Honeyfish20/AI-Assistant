from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    model_id = models.CharField(max_length=255)
    max_tokens = models.IntegerField(default=8192, help_text="Global Setting")
    stop_sequences = models.TextField(blank=True, null=True, help_text="Global Setting")
    temperature = models.FloatField(default=0, help_text="Global Setting")
    region = models.TextField(default="us-east-1", help_text="Global Setting")
    
    class Mate:
        verbose_name = "Large language models"
        verbose_name_plural = "Large language models"
        app_label = "assistant_settings"
    
    def __str__(self):
        return str(self.model_id)
