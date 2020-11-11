from rest_framework import serializers
# from backend.accounts.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class GeneralUserSerializer(serializers.ModelSerializer):
    # user_profile = serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'nickname', 
            'last_name', 
            'first_name', 
            'avatar_url', 
            'description', 
            # 'user_profile'
            ]

    # def get_user_profile(self, obj):
    #     user_profile = UserProfile.objects.filter(user__id=obj.id).first()
    #     return SocialMediaSerializer([user_profile,], many=True).data[0]

from rest_framework_gis.serializers import GeoFeatureModelSerializer

class UpdateLocationSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = User
        geo_field = "coordinates"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('id','email','coordinates',)

class NearbyUsersSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = User
        geo_field = "coordinates"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('id','first_name', 'last_name', 'address', 'coordinates',)

