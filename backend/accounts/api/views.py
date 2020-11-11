import decimal
import random
from ipware import get_client_ip
from backend.accounts.models import User
from rest_framework.generics import (ListAPIView, UpdateAPIView)
from backend.accounts.api.serializers import GeneralUserSerializer, UpdateLocationSerializer, NearbyUsersSerializer
from django.conf import settings

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
from django.contrib.gis.geos import GEOSGeometry
import json
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
        print('Users latitude {} and longitude {}'.format(latitude, longitude))

        # For GeoDjango PointField we define it y and x, contrary to what is a norm
        # more in docs: https://docs.djangoproject.com/en/3.1/ref/contrib/gis/geos/#point
        point = Point(float(longitude), float(latitude), srid=4326)
        
        # Requires at least 1 user in DB (e.g.  admin) 
        user_obj = User.objects.all().first()
        anonymize_profile = UpdateLocationSerializer(user_obj, data={'coordinates': point}, partial=True)
        if not anonymize_profile.is_valid():
            return Response(anonymize_profile.errors, status=status.HTTP_400_BAD_REQUEST)
        anonymize_profile.save()

        pnt = GEOSGeometry(point)
        geojson = json.loads(pnt.geojson)
        return Response({'coordinates': reversed(geojson['coordinates'])}, status=status.HTTP_201_CREATED)
    

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
        # float(random.randrange(155, 389))/100 # Other way of doing things
        # randomizing values and cutting decimals to 6
        lat, lng = round((float(lat) + random_lat),
                         6), round((float(lng) + random_lng), 6)
        return lat, lng

from geopy.geocoders import Nominatim
from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis import filters as geofilters
from django.db.models import Q
from django.contrib.gis.measure import Distance

class GetCoordinatesFromAddress(ListAPIView, GeoFilterSet):
    """ Shows nearby Users"""
    
    def get(self, *args, **kwargs):
        # We can check on the server side the location of the users, using request
        # point = self.request.user.coordinates
        # ?address=QUERY_ADDRESS
        # QUERY_ADDRESS is the information user passes to the query
        QUERY_ADDRESS = self.request.query_params.get('address', None)
        
        if QUERY_ADDRESS not in [None, '']:
            # here we can use the geopy library:
            geolocator = Nominatim(user_agent="mysuperapp")
            location = geolocator.geocode(QUERY_ADDRESS)
            return Response({'coordinates': [location.latitude ,location.longitude]}, status=status.HTTP_200_OK)
        else: 
            return Response({'message': 'No address was passed in the query'}, status=status.HTTP_400_BAD_REQUEST)
            

class ListNearbyUsers(ListAPIView, GeoFilterSet):
    """ Shows nearby Users"""
    model = User
    serializer_class = NearbyUsersSerializer
    pagination_class = GeoJsonPagination
    contains_geom = geofilters.GeometryFilter(name='coordinates', lookup_expr='exists')
    
    def get_queryset(self, *args, **kwargs):
        # We can check on the server side the location of the users, using request
        # point = self.request.user.coordinates
        # ?address=QUERY_ADDRESS
        # QUERY_ADDRESS is the information user passes to the query
        QUERY_ADDRESS = self.request.query_params.get('address', None)
        queryset = []

        if QUERY_ADDRESS not in [None, '']:
            queryset = User.objects.all()
            # here we can use the geopy library:
            geolocator = Nominatim(user_agent="mysuperapp.com")
            location = geolocator.geocode(QUERY_ADDRESS)

            # Let's use the obtained information to create a geodjango Point
            point = Point(float(location.longitude), float(location.latitude), srid=4326)
            # and query for 10 Users objects to find active users within radius
            queryset = queryset.filter(Q(coordinates__distance_lt=(
                point, Distance(km=settings.RADIUS_SEARCH_IN_KM))) & Q(is_active=True)).order_by('coordinates')[0:10]
            return queryset
        else: 
            return queryset
            
