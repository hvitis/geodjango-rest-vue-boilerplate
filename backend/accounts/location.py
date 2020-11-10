# from djoser.views import UserViewSet as BaseUserViewSet
from django.conf import settings
from accounts.models import User
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, UpdateAPIView)
from core.restconf.djoser.serializers import CustomUserSerializer, CustomUsersSerializer
from accounts.models import TemporaryProfile
from accounts.api.serializers import TemporaryProfileSerializer, InitializeProfileSerializer, IsFirstLoginProfileSerializer
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework import permissions
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance as ClosestDistance
from rest_framework.exceptions import APIException, ValidationError
from core.common.logger import log
import decimal
import random
from django.http import JsonResponse
from django.db.models import Q
from mail.tasks import sendRenderedEmailTemplate
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import GEOSGeometry
from rest_framework.decorators import api_view



from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView

from accounts.api.serializers import UploadPhotoSerializer
import base64

from django.core.files.base import ContentFile


class UploadPhotoAPIView(UpdateAPIView):
    parser_class = (FileUploadParser,)
    model = User
    queryset = User.objects.all()
    serializer_class = UploadPhotoSerializer
    lookup_field = 'nickname'

    def get_queryset(self):
        print('queryset', self.request.user.nickname)
        qs = User.objects.filter(nickname=self.request.user.nickname).first()
        return qs

    def put(self, request, nickname, *args, **kwargs):
        snippet = User.objects.filter(nickname=nickname).first()
        print('avatar', request.data['avatar'])
        formated, imgstr = request.data['avatar'].split(';base64,')
        ext = formated.split('/')[-1]
        # You can save this as file instance.
        avatar_file = ContentFile(base64.b64decode(imgstr), name='user_{}.'.format(self.request.user.nickname) + ext)
        request.data['avatar'] = avatar_file
        if snippet is None:
            return Response({'message': 'User does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        file_serializer = UploadPhotoSerializer(snippet, data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSetAll(ListAPIView):
    serializer_class = CustomUsersSerializer
    queryset = User.objects.all()
    permission_classes = []


class UserViewSet(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()
    permission_classes = []

    def get_queryset(self):
        nickname = self.kwargs.get("nickname", None)
        if nickname is None:
            return User.objects.all()
        return User.objects.filter(nickname=nickname)


class TemporaryProfileApiView(CreateAPIView):
    """ Creates a new email user with geolocation and returns 
    10 closest people to the person"""
    model = TemporaryProfile
    serializer_class = TemporaryProfileSerializer
    pagination_class = GeoJsonPagination

    def perform_create(self, request, *args, **kwargs):
        """Changing coordination to the annonimized one and
        saving with serializer

        Args:
            request ([object]): {
            "email": String,
            "nickname": String,
            "coordinates": "POINT (${latitude} ${longitude})",
            "is_printer": Boolean
        }
        """
        request = request.data
        print('COORD', request['geometry'])
        if request['geometry'] == None:
            raise ValidationError(
                'Coordinates field required!', code=400)
        latitude, longitude = request['geometry']['coordinates']
        latitude, longitude = self.anonimize_location(latitude, longitude)
        request['geometry']['coordinates'] = [latitude, longitude]
        anonimized_profile = TemporaryProfileSerializer(data=request)
        anonimized_profile.is_valid()
        anonimized_profile.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        request = request.data
        print('Request daata: ', request)
        response_obj = {"data": []}

        # Formatting recieved string to lat, lng
        # Recieving str format: POINT (lan lng)
        latitude, longitude = request['coordinates'].split(
            "POINT (")[1].split(")")[0].split(" ")
        point = Point(float(latitude), float(longitude), srid=4326)

        # Querying for potential customers or printers, depending of recieved request
        queryset = TemporaryProfile.objects.filter(Q(coordinates__distance_lt=(
            point, Distance(km=settings.FREE_RADIUS_SEARCH))) & Q(is_printer=(not request['is_printer']))).order_by('coordinates')[0:10]

        email_name_list = []
        for obj in queryset:
            email_name_list.append(
                {'email': obj.email})
        main_message = 'Here you have a list of users that you may reach out to.'
        response_obj['data'] = email_name_list
        if len(email_name_list) == 0:
            response_obj['message'] = "We got you! Currently there is nobody in your neighbourhood. We will send you an e-mail if somebody will appear nearby."
            return Response(response_obj, status=status.HTTP_200_OK)
        if request['is_printer']:
            try:
                response_obj['message'] = "We have sent you list of people searching for 3D printers specialists!"
            except ValueError or KeyError:
                raise ValidationError(
                    'Sending e-mail failed. Please contact with the administrator!', code=400)
        else:
            try:
                response_obj['message'] = "We have sent you list of people willing to 3D print for you."
            except ValueError or KeyError:
                raise ValidationError(
                    'Sending e-mail failed. Please contact with the administrator!', code=400)
        return Response(response_obj, status=status.HTTP_200_OK)

    def anonimize_location(self, lat, lng):
        """Shifting lat and lng a random tens of meters in positive direction
            Three decimal places will always be within 80 m of the point described. 
            This is specific enough already for the smallest towns and even large buildings.
        Args:
            lat ([type]): [description]
            lng ([type]): [description]

        Returns:
            [lat and lng]: [returns anonimized lat and lng as rounded floats]
        """
        random_lat = float(decimal.Decimal(
            random.randrange(50, 90)) / 10000)
        random_lng = float(decimal.Decimal(
            random.randrange(50, 90)) / 10000)
        print(random_lat, random_lng)
        # float(random.randrange(155, 389))/100 # Other way of doing things
        # randomizing values and cutting decimals to 6
        lat, lng = round((float(lat) + random_lat),
                         6), round((float(lng) + random_lng), 6)
        return lng, lat


class InitializeProfileApiView(UpdateAPIView):
    """ Updating values is_printer is_designer is_customer and localisation
    when user is loggin for the first time"""
    model = User
    serializer_class = InitializeProfileSerializer
    pagination_class = GeoJsonPagination
    queryset = User.objects.all()
    lookup_field = 'nickname'


class IsFirstLoginAPIView(APIView):
    """ Updating values is_printer is_designer is_customer and localisation
    when user is loggin for the first time"""
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IsFirstLoginProfileSerializer
 
    def get(self, request, *args, **kwargs):
        qs = User.objects.filter(nickname=self.request.user.nickname).first()
        print('Hello')
        return Response({"is_first_login": qs.first_login()}, status=status.HTTP_200_OK)


# @api_view(['GET'])
# def IsFirstLoginAPIView(request):
#     return Response({"message": "Hello, world!"})
