from django.urls import path
from backend.accounts.api.views import UserViewSet, UserViewSetAll

app_name = 'accounts'

urlpatterns = [
    path('',
         UserViewSetAll.as_view(), name="user-profiles"),
    path("<int:user_id>",
         UserViewSet.as_view(), name="user-profile"),
]
