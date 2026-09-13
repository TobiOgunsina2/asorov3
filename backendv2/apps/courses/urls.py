from django.urls import path
from .views import UnitList

urlpatterns = [
    path('units/', UnitList.as_view(), name='unit-list')
]