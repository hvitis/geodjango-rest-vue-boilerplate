from django.db import models
from rest_framework import serializers


class Post(models.Model):
    subject = models.CharField(max_length=200)
    body = models.TextField()


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'subject', 'body', 'pk')
