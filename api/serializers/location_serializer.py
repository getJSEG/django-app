from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from drf_extra_fields.fields import Base64ImageField

from ..models import Location
from ..models import CustomUser

# TESTING ONLY
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

#Creating LOCATION
#MODIFI 
class CreateLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('locationType', 'incharge', 'email', 'address', 'city', 'department', 'storeNumber',
                  'country','status', 'cost_center', 'dateCreated', 'tax', 'isPreTax')
        extra_kwargs = {
            "tax": { "required" : False },
            "isPreTax": { "required" : False }, 
            "email": { "required" : False },
            "phone": { "required" : False }
        }

        email = serializers.EmailField()
        
    def validate(self, attrs):
        lower_email = attrs.get('email', '').strip().lower()
        incharge = attrs.get('incharge', '').title()
        address = attrs.get('address', '').title()
        department = attrs.get('department', '').title()
        city = attrs.get('city', '').title()
        country = attrs.get('country', '').title()
        location_type = attrs.get('locationType', '').title()
        status = attrs.get('status', '').strip().title()

        # if Locations.objects.filter(email__iexact=lower_email).exists():
        #     raise serializers.ValidationError("Duplicate")
        
        attrs['incharge'] = incharge 
        attrs['address'] = address
        attrs['city'] = city
        attrs['department'] = department
        attrs['country'] = country
        attrs['locationType'] = location_type
        attrs['status'] = status
        attrs['email'] = lower_email

        return attrs
    

class UpdateLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('incharge', 'email', 'phone', 'status','profit_center', 'address', 'city', 'department',
                   'tax', 'isPreTax')
    
    def validate(self, attrs):

        for key in attrs:
            if key == 'email':
                temp = attrs[key].strip().lower()
                attrs[key] = temp
                
            if key == 'incharge' or key == 'address' or key == 'department' or key == 'city' or key == 'status':
                temp = attrs[key].title()
                attrs[key] = temp

        return attrs