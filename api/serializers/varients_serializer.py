from rest_framework import serializers
from ..models import Varient, VarientColor

#varient colors
class VarientColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = VarientColor
        fields = ['id', 'color', 'image']
        extra_kwargs = {
            "id": { "required" : False },
            "color": { "required" : True },
            "image": { "required" : False },
        }

    def validate(self, attrs):
        if "color" in attrs:
            description = attrs.get('color').title()
            attrs['color'] = description
    
        return attrs
 
#Varient
class CreateVarientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Varient
        fields = ['id', 'size', 'sku', "price", "varient_color", 'units',
                  'storage_location', 'status']
        
        extra_kwargs = {
            "storage_location":  { "required" : False },
            "status": { "required" : False },
            "id": {"required" : False },
            "varient_color": {"required": False}
        }

    def validate(self, attrs):
        if "status" in attrs:
            name = attrs.get('status').title()
            attrs['status'] = name

        return attrs

#
class UpdatedVarientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Varient
        fields = ['size', 'units', 'sku', 'price', 'status', 'storage_location']
        
    def validate(self, attrs):
        if "status" in attrs:
            name = attrs.get('status').title()
            attrs['status'] = name

        return attrs
