from rest_framework import serializers
from apps.profiles.models import Profile


class ProfileSerializer(serializers.Serializer):
    email = serializers.CharField(source="user.email", read_only=True)
    class Meta:
        model = Profile
        fields = ["id", "email", "display_name", "xp", "streak"]
    
