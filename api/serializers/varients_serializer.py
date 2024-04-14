from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from drf_extra_fields.fields import Base64ImageField

from ..models import Varients, VarientImages, ImageAlbum, VarientColors

####CREATING#####

#varient colors
class CreateVarientColorsSerializer(serializers.ModelSerializer):
    color = serializers.ImageField()

    class Meta:
        model = VarientColors
        fields = ['color', 'description', 'album']
        extra_kwargs = {
            "color": { "required" : True },
            "album": { "required" : True },
            "description": { "required" : True },
        }

    def validate(self, attrs):
        if "description" in attrs:
            description = attrs.get('description').title()
            attrs['description'] = description
    
        return attrs

#varient Images
class CreateVarientImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    
    class Meta:
        model = VarientImages
        fields = ['image', 'album']

class UpdateVarientImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    
    class Meta:
        model = VarientImages
        fields = ['image', 'album']
#Varient
class CreateVarientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Varients
        fields = ['location_id', 'product_id', 'name', 'brand', 'vendor_sku',
                  'size', 'sku', 'album', 'units', 'purchase_price', 'listed_price',
                  'storage_location', 'status']
        extra_kwargs = {
            "vendor_sku": { "required" : False },
            "storage_location":  { "required" : False },
            "status": { "required" : False },
        }

    def validate(self, attrs):
        if "name" in attrs:
            name = attrs.get('name').title()
            attrs['name'] = name
        if "brand" in attrs:
            name = attrs.get('brand').title()
            attrs['brand'] = name
        if "status" in attrs:
            name = attrs.get('status').title()
            attrs['status'] = name

        return attrs

    def create(self, validated_data):

        product_varient = Varients.objects.create(**validated_data) # creating produc

        return product_varient



####UPDATING#####
#vareints colors Serializer for Updating
class UpdateVarientColorsSerializer(serializers.ModelSerializer):
    color = serializers.ImageField()
    class Meta:
        model = VarientColors
        fields = ['color', 'description']
        extra_kwargs = {
            "color": { "required" : False },
            "description": { "required" : False },
        }

    def validate(self, attrs):
        if "description" in attrs:
            description = attrs.get('description').title()
            attrs['description'] = description

        return attrs

#ALBUM
class UpdatedVarientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Varients
        fields = ['location_id', 'product_id', 'name', 'brand', 'vendor_sku',
                  'size', 'sku', 'album', 'units', 'purchase_price', 'listed_price',
                  'storage_location', 'status']
        extra_kwargs = {
            "name":  { "required" : False },
            "units": { "required" : False },
            "size":  { "required" : False },
            "brand": { "required" : False },
            "vendor_sku": { "required" : False },
            "sku":  { "required" : True },
            "purchase_price": { "required" : False },
            "listed_price": { "required" : False },
            "storage_location":  { "required" : False },
            "status": { "required" : False },
        }
    def validate(self, attrs):
        if "name" in attrs:
            name = attrs.get('name').title()
            attrs['name'] = name
        if "brand" in attrs:
            name = attrs.get('brand').title()
            attrs['brand'] = name
        if "status" in attrs:
            name = attrs.get('status').title()
            attrs['status'] = name

        return attrs







#GETTING
class GetVarientImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = VarientImages
        fields = ['image', 'album']

class GetVarientColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = VarientColors
        fields = ['color', 'description']

class GetAlbumSerializer(serializers.ModelSerializer):
    images = GetVarientImageSerializer(many=True)
    varient_colors = GetVarientColorSerializer(many=True)
    
    class Meta:
        model = ImageAlbum
        fields = ['images', 'varient_colors']


class GetVarientSerializers(serializers.ModelSerializer):
    album = GetAlbumSerializer()
    total_stock_item_price = serializers.CharField(source='cal_purchase_price')

    class Meta:
        model = Varients
        fields = '__all__'
        read_only_fields = ['id', 'name', 'size', 'units', 'sku', 'album', 'total_stock_item_price']




