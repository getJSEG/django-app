from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from drf_extra_fields.fields import Base64ImageField

from ..models import Locations
from ..models import CustomUser
from ..models import Products, Varients, VarientImages, VarientColors, ImageAlbum



################################ LOCATION ################################
##########################################################################
# TESTING ONLY
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'

#Creating LOCATION
#MODIFI 
class CreateLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ('location_type', 'incharge', 'email', 'address', 'city', 'department', 'store_number',
                  'country','status','profit_center', 'cost_center', 'status_date', 'local_tax', 'pre_tax_items')
        extra_kwargs = {
            "local_tax": { "required" : False },
            "pre_tax_items": { "required" : False }, 
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
        location_type = attrs.get('location_type', '').title()
        status = attrs.get('status', '').strip().title()

        # if Locations.objects.filter(email__iexact=lower_email).exists():
        #     raise serializers.ValidationError("Duplicate")
        
        attrs['incharge'] = incharge 
        attrs['address'] = address
        attrs['city'] = city
        attrs['department'] = department
        attrs['country'] = country
        attrs['location_type'] = location_type
        attrs['status'] = status
        attrs['email'] = lower_email

        return attrs
    

class UpdateLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locations
        fields = ('incharge', 'email', 'phone', 'status','profit_center', 'address', 'city', 'department',
                  'cost_center', 'status_date', 'local_tax', 'pre_tax_items')
    
    def validate(self, attrs):


        for key in attrs:
            if key == 'email':
                temp = attrs[key].strip().lower()
                attrs[key] = temp
                
            if key == 'incharge' or key == 'address' or key == 'department' or key == 'city' or key == 'status':
                temp = attrs[key].title()
                attrs[key] = temp

        return attrs