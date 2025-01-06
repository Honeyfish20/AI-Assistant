from rest_framework import viewsets
from .models import BaseModel
from .serializers import BaseModelSerializer

class BaseModelsViewSet(viewsets.ModelViewSet):
    queryset = BaseModel.objects.all()
    serializer_class = BaseModelSerializer