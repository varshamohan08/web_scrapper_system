from django.urls import path
from .views import *

urlpatterns = [
    path('save-entity', SaveEntitiesMaster.as_view(), name='save-entity'),
    path('get-entity', GetEntitiesMaster.as_view(), name='get-entity'),
]