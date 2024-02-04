from rest_framework import serializers
from .models import Locations, LocationUsers

# THIS IS FOR GETTIN THE LOCATION INFORMATION
class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ('id', 'location_type', 'location', 'incharge', 'email', 'users', 'country',
                  'address', 'profit_center', 'cost_center', 'status', 'status_date')

#THIS IS FOR CREATING LOCATION
class CreateLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ('location_type', 'location', 'incharge', 'email', 'users', 'country',
                 'address', 'profit_center', 'cost_center', 'status',
                  'status_date')
        
# THIS IS FOR GETTIN USER INFORMATION
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationUsers
        fields = ('username', 'name', 'title', 'superUser', 'employee', 'status_date')

# #  THIS IS FOR CREATING USERS
class CreateUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationUsers
        fields = ('username', 'password', 'name', 'title', 'superUser', 'employee', 'status_date')
