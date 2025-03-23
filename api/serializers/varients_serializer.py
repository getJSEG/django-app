from rest_framework import serializers

# Models
from ..models import Varient, Product, Images

# ['product', 'color', 'size', 'units', 'minUnits', 'price', 'categories', 'image', 'vendorSku', 'storageLocation', 'sku', 'location_id']

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = ['link']
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'brand']

class retrivingProductSerialzier(serializers.ModelSerializer):
    product = ProductSerializer()
    varientImage = ImageSerializer()

    class Meta:
        model = Varient
        fields = '__all__'
