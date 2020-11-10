from rest_framework import serializers
from backend.posts.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'subject', 'body', 'pk')
