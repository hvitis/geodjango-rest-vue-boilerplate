import decimal
import random
from ipware import get_client_ip
from django.contrib.auth.models import Permission
from backend.accounts.models import User
from rest_framework.generics import (ListAPIView, UpdateAPIView)
from backend.accounts.api.serializers import GeneralUserSerializer, UpdateLocationSerializer


class UserViewSetAll(ListAPIView):
    serializer_class = GeneralUserSerializer
    queryset = User.objects.all()
    permission_classes = []

from rest_framework_gis.pagination import GeoJsonPagination
from backend.utils.coordinates import get_lat_lng_from_ip
from rest_framework import status
from rest_framework.response import Response
# from backend.accounts.api.serializers import UpdateLocationSerializer
from django.contrib.gis.geos import Point

class UpdateLocation(UpdateAPIView):
    """ Creates a new email user with geolocation and returns 
    10 closest people to the person"""
    model = User
    serializer_class = UpdateLocationSerializer
    pagination_class = GeoJsonPagination
 

    def update(self, request, *args, **kwargs):
        """Here we can e.g. 
        - get location from the IP
        - change coordinates to a randomly
        close one in order to anonymize users location.
        Args:
            request ([object]): {
            "coordinates": "POINT (${latitude} ${longitude})",
        }
        """
        # response = super().create(request, *args, **kwargs)
        
        client_ip, is_routable = get_client_ip(request)
        latitude, longitude = get_lat_lng_from_ip(client_ip)
        if not latitude:
            return Response({'message': 'IP or location was not found.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        latitude, longitude = self.anonymize_location(latitude, longitude)
        print('latitude, longitude', latitude, longitude)
        point = Point(float(latitude), float(longitude), srid=4326)
        # Requires at least 1 user in DB (e.g.  admin) 
        user_obj = User.objects.all().first()
        new_coordinates = {'coordinates': point}
        anonymize_profile = UpdateLocationSerializer(user_obj, data=new_coordinates, partial=True)
        if not anonymize_profile.is_valid():
            return Response(anonymize_profile.errors, status=status.HTTP_400_BAD_REQUEST)
        anonymize_profile.save()
        return Response(anonymize_profile.data, status=status.HTTP_201_CREATED)
    
        # Querying for potential customers or printers, depending of recieved request
        # queryset = TemporaryProfile.objects.filter(Q(coordinates__distance_lt=(
        #     point, Distance(km=settings.FREE_RADIUS_SEARCH))) & Q(is_printer=(not request['is_printer']))).order_by('coordinates')[0:10]
    
    def anonymize_location(self, lat, lng):
        """Shifting lat and lng a random tens of meters in positive direction
            Three decimal places will always be within 80 m of the point described. 
            This is specific enough already for the smallest towns and even large buildings.
        Args:
            lat ([number]): [Latitude]
            lng ([number]): [Longitude]

        Returns:
            [lat, lng]: [returns anonimized lat and lng as rounded floats]
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
        print(lat, lng)
        return lng, lat