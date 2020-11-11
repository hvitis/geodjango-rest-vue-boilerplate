from django.urls import path
from backend.accounts.api.views import UserViewSetAll, UpdateLocation, ListNearbyUsers

app_name = 'accounts'

urlpatterns = [
    path('',
         UserViewSetAll.as_view(), name="user-profiles"),
    path("location",
         UpdateLocation.as_view(), name="update-location"),
    path("nearbyusers",
         ListNearbyUsers.as_view(), name="nearby-users"),

]
