from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from ipware import get_client_ip

from backend.posts.models import Post
from backend.posts.api.serializers import PostSerializer

from django.http.response import JsonResponse

def show_user_ip(request):
    client_ip, is_routable = get_client_ip(request)
    res = {
        'client_ip': client_ip,
        'is_routable': is_routable
    }
    return JsonResponse(res)


# Serve Vue Application
index_view = never_cache(TemplateView.as_view(template_name='index.html'))


class PostsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Postss to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ListPosts(ListAPIView):
    """
    API endpoint that allows Postss to be viewed or edited.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    def get(self, request):
        client_ip, is_routable = get_client_ip(request)
        data = {
            'client_ip': client_ip,
            'is_routable': is_routable
        }
        return Response(data, status=status.HTTP_208_ALREADY_REPORTED)