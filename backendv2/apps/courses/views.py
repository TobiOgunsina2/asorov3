from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Unit
from .serializers import UnitSerializer
# Create your views here.

class UnitList(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.AllowAny]

