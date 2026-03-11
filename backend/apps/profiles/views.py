from django.shortcuts import render

from apps.profiles.models import Profile
from apps.profiles.serializer import ProfileSerializer
from rest_framework.views import APIView, Response
from rest_framework import permissions, status


# Create your views here.
# User profile view - shows public profile info, XP, streaks, etc. Can be extended to include things like user-created content, social features, etc.

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = Profile.objects.get(user=request.user)
        user_data = ProfileSerializer(user).data
        return Response(status=status.HTTP_200_OK, data={'user_data': user_data})

