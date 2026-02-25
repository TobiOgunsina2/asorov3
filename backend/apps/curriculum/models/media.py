from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Media can be audio, video or an image. 
# For slides: This allows for media to be played
# For phrases, words, sentences: this gives extra content for users to understand

class Media(models.Model):
    MEDIA_TYPE_CHOICES = [("audio", "Audio"), ("video", "Video"), ("image", "Image")]
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to="media/") #change this should point to a location on the cloud
    description = models.CharField(max_length=255, blank=True)