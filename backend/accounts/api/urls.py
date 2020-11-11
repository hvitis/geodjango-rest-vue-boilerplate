from django.urls import path
from backend.accounts.api.views import UserViewSetAll, UpdateLocation, ListNearbyUsers, GetCoordinatesFromAddress

app_name = 'accounts'

urlpatterns = [
    path('',
         UserViewSetAll.as_view(), name="user-profiles"),
    path("location",
         UpdateLocation.as_view(), name="update-location"),
    path("nearbyusers",
         ListNearbyUsers.as_view(), name="nearby-users"),
    path("coordinates",
         GetCoordinatesFromAddress.as_view(), name="get-coordinates"),

]
