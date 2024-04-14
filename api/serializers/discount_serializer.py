from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from drf_extra_fields.fields import Base64ImageField

from ..models import Discount



################################ LOCATION ################################
##########################################################################
# TESTING ONLY
class CreateDisocuntSerializer(serializers.ModelSerializer):
    expiration = serializers.DateTimeField(input_formats=['%m-%d-%Y'])

    class Meta:
        model = Discount
        fields = ['location', 'discount_code', 'discount', 'expiration', 'description']
        extra_kwargs = {
            "location": { "required" : False },
        }

class GetDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'