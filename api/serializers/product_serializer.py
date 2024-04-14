from datetime import datetime
from rest_framework import serializers

from ..models import CustomUser
from ..models import Products

################################ PRODUCT ################################
#########################################################################
class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('name', 'brand')
    
    def validate(self, attrs):
        user = self.context['request'].user

        get_user = CustomUser.objects.filter(username=user)
        
        if not get_user.exists():
            raise serializers.ValidationError("user not found") 
        return attrs
        
    def create(self, validated_data):
        username = self.context['request'].user
        user = CustomUser.objects.filter(username=username)
        product = Products.objects.create(**validated_data, location_id=user[0].location)
        return product

class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class Update(serializers.ModelSerializer):
    class Meta: 
        model = Products
        fields = ['name', 'brand', 'product_acronym', "status"]
        extra_kwargs = {
            "product_acronym": { "required" : False },
            "status": { "required" : False },
        }

    def validate(self, attrs):
        if "name" in attrs:
            name = attrs.get('name').title()
            attrs['name'] = name

        if "brand" in attrs:
            attrs['brand'] = attrs.get('brand').title()
        
        if "product_acronym" in attrs:
            attrs['product_acronym'] = attrs.get('product_acronym').title()

        if "status" in attrs:
            attrs['status'] = attrs.get('status').title()

        return attrs


    def update(self, instance, validated_data):
        instance.status_date = datetime.now() 
        instance = super().update(instance, validated_data)
        return instance