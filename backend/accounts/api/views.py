# from djoser.views import UserViewSet as BaseUserViewSet


from backend.accounts.models import User
from rest_framework.generics import (ListAPIView)
from backend.accounts.api.serializers import GeneralUserSerializer

from django.core.files.base import ContentFile


class UserViewSetAll(ListAPIView):
    serializer_class = GeneralUserSerializer
    queryset = User.objects.all()
    permission_classes = []



