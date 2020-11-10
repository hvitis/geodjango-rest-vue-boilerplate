
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework import permissions
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance as ClosestDistance
from rest_framework.exceptions import APIException, ValidationError
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import GEOSGeometry