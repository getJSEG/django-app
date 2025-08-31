from rest_framework import serializers

# Models
from ..models import Varient, Product, Images, Categories, Tags

# ['product', 'color', 'size', 'units', 'minUnits', 'price', 'categories', 'image', 'vendorSku', 'storageLocation', 'sku', 'location_id']

class categoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['categorie']

class tagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ['tag']

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
    categories = categoriesSerializer(many=True, read_only=True)
    tags = tagsSerializer(many=True, read_only=True)

    class Meta:
        model = Varient
        fields = '__all__'
