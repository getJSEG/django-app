from datetime import datetime
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import validators

# Models
from ..models import Product, ProductAttribute, Varient, VarientColor, Tags
from ..models import ImageAlbum, ProductImages

# Exceptions
from ..exceptions import ProductExeption, CustomException
# Product Images
class ProductImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = ['id', 'album', 'images']

    def validate(self, attrs):
        # TODO: ADD MORE VALIDATI
        images = attrs.get('images')
        print(images)
        return attrs
    
class ImageAlbumSerializer(serializers.ModelSerializer):
    images = ProductImagesSerializer( many=True)
    class Meta:
        model =  ImageAlbum
        fields = '__all__'

# Creating product
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'location_id', 'item_cost', 'created_by', 'price', 'product_acronym', 'status']
        extra_kwargs = {
            "name": { "required" : True },
            "brand": { "required" : True },
            "item_cost": { "required" : True },
            "created_by": { "required" : True },
            'id': { "required" : False },
            'price': { "required": True },
            "product_acronym": { "required" : False },
            "status": { "required" : False },
        }
    
    def validate(self, attrs):
        price = attrs.get('price')

        print(price)

        if "name" in attrs:
            attrs['name'] = attrs.get('name').title()
        if "brand" in attrs:
            attrs['brand'] = attrs.get('brand').title()
        if "product_acronym" in attrs:
            attrs['product_acronym'] = attrs.get('product_acronym').title()
        if "status" in attrs:
            attrs['status'] = attrs.get('status').title()
            
        # if Decimal(price) < 0 :
        #     raise CustomException({'message': price + "need to be grater that 0"})
        
        return attrs
    
    def create(self, validated_data):
        album = ImageAlbum.objects.create()
        
        product = Product.objects.create(**validated_data, album=album)

        return product
    
    def update(self, instance, validated_data):
        instance.status_date = datetime.now() 
        instance = super().update(instance, validated_data)
        return instance


# Retrive Products
class GetProductSerializer(serializers.ModelSerializer):
    album = ImageAlbumSerializer()
    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'price', 'item_cost', 'created_by', 'album', 'location_id', 'created_on')


class TagsSerializer(serializers.ModelSerializer): 

    # def validate(self, value):
    #     for validator in self.validators:
    #         if isinstance(validator, validators.UniqueTogetherValidator):
    #             self.validators.remove(validator)
    #     super(TagsSerializer, self).run_validators(value)

    def create(self, validated_data):
        instance, _ = Tags.objects.get_or_create(**validated_data)
        return instance

    class Meta:
        model = Tags
        fields = ["tag"]
        extra_kwargs = {
            'tag': {'validators': []},
        }

class ProductAttributes(WritableNestedModelSerializer):
    product = ProductSerializer()
    tags = TagsSerializer(required=False, many=True)
    # varients = GetVarientSerializer(many=True)

    class  Meta:
        model = ProductAttribute
        fields = ['product', 'tags']
        extra_kwargs = {
            'tags': {'validators': []},
        }





class GetVarientColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = VarientColor
        fields = '__all__'

# THIS MIGHT GET REMOVED
class GetVarientSerializer(serializers.ModelSerializer):
    varient_color = GetVarientColorSerializer()
    class  Meta:
        model = Varient
        fields = ['id', 'price', 'status', 'size', 'units', 'sku', 'varient_color']

# This is for list 
class getTags(serializers.ModelSerializer):
    class Meta: 
        model = Tags
        fields = ['tag']

# Rename this to GetSingle ProductSttribute Serializer
# THIS IS FOR SINGLE ITEMS
class GetProductAttributes(serializers.ModelSerializer):
    product = GetProductSerializer()
    varients = GetVarientSerializer(many=True)
    tags = getTags(many=True)

    class  Meta:
        model = ProductAttribute
        fields = ('product','varients', 'tags')

# This is for list 
class getVarientInformation(serializers.ModelSerializer):
    class Meta: 
        model = Varient
        fields = ['id', 'price', 'size', 'units', 'sku']

# Rename this to Get Product AttributesSerializer 
class GetProductReducedSerializer(serializers.ModelSerializer):
    product = GetProductSerializer()
    varients = getVarientInformation(many=True)
    varientInProduct = serializers.CharField(source='varient_count')
    totalValue = serializers.JSONField(source='totalVarientValue')
    tags = getTags(many=True)

    class  Meta:
        model = ProductAttribute
        fields = ('product', 'varients', 'tags', 'varientInProduct', "totalValue",)








# THIS IS FOR POS ONLY Retriving only SPECIFIC INFORMATION
class getProductReduceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'brand')

# THIS MIGHT GET REMOVED
class getVarientReduceInforSerializer(serializers.ModelSerializer):
    varient_color = GetVarientColorSerializer()
    class  Meta:
        model = Varient
        fields = ['price','size', 'units', 'sku', 'varient_color', 'status']

class getProductAttributePOSSerializer(serializers.ModelSerializer):
    product = getProductReduceInfoSerializer()
    varients = getVarientReduceInforSerializer(many=True)
    tags = getTags(many=True)

    class  Meta:
        model = ProductAttribute
        fields = ('product','varients', 'tags')