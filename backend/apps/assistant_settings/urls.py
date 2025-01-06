from django.urls import include, path
from rest_framework import routers
from .views import BaseModelsViewSet

router = routers.DefaultRouter()
router.register(r'base_models', BaseModelsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
