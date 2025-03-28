from datetime import datetime
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


# Models
from ..models import Product, Varient, Tags, Images, Categories
from ..helper import generate_sku
#Varient

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'

class ImageSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model= Images
        fields = '__all__'

# TODO: This field "varientImage" should not trow error 
# TODO: get the Id of  the created Product
class VariantSerializer(WritableNestedModelSerializer):
    varientImage = ImageSerialzier(required=False)
    sku = serializers.CharField(read_only=True)
    id = serializers.CharField(required=False)

    class Meta:
        model= Varient
        fields = ['id', 'color', 'size', 'units', 'minUnits', 'sku', 'price', 'tags', 'categories', 'varientImage']
        optional_fields = ['varientImage' ]
        extra_kwargs = {
            "id": { "required" : False },
            "tags": { "required" : False },
            "categories": { "required" : False },
            "varientImage": { "required" : False },
            # 'sku': {'error_messages': {'unique': 'Ya Existe un variente con la misma informacion'} }
        }

    
class productSerializer(WritableNestedModelSerializer):
    variants = VariantSerializer(many=True)
    total_varients = serializers.IntegerField(read_only=True)
    average_price = serializers.DecimalField(max_digits=9, decimal_places=2,read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            "id": { "required" : False },
            "productAcronym": { "required" : False },
            'name': {'error_messages': {'blank': 'Campo no debe estar vacío'} },
            'brand': {'error_messages': {'blank': 'Campo no debe estar vacío'} },
            'cost': {'error_messages': {'blank': 'Campo no debe estar vacío', 'invalid': 'Introduce un precio válido' } }
        }
        # TODO: CHECK If the items exist before cleaning name and brand if not
        # When updating if not it will update it at empty string
    def validate(self, attrs):
        if 'name' in attrs:
            attrs['name'] = attrs.get('name', '').strip().title().lstrip(",.-=/><;|")
        if 'brand' in attrs:
            attrs['brand'] = attrs.get('brand', '').strip().title().lstrip(",.-=/><;|")
        return attrs
    
    # # This updates the name  and all of the Sku items relates to this product
    def update(self, instance, validated_data):
        variants_data =  validated_data.pop('variants')

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        existing_children_ids = [child.id for child in instance.variants.all()]
        incoming_children_ids = []
        # If the user provides a child id then update all the field that where provided.
        for variant in variants_data:
            child_id = variant.get('id')
            if child_id:
                # Update existing child
                child = Varient.objects.get(pk=child_id)
                for key, value in variant.items():
                    setattr(child, key, value)
                child.save()
                incoming_children_ids.append(child_id)
                #Add Create if the product does not have a 'ID'
        # 
        if 'name' or 'brand' in validated_data:
            for child_id in set(existing_children_ids) - set(incoming_children_ids):
                child = Varient.objects.get(id=child_id)
                sku_code = generate_sku(instance.name, instance.brand, child.size, child.color, instance.id)
                setattr(child, 'sku', sku_code)
                child.save()

        return instance


    # Creates variantes
    def create(self, validated_data):
        variants = validated_data.pop("variants")
        product_ = Product.objects.create(**validated_data)

        for variant in variants:
            sku_code = generate_sku(product_.name, product_.brand, variant['size'], variant['color'], product_.id)

            if 'varientImage' in variant:
                image = variant.pop("varientImage")
                img = Images.objects.create(**image)
                variant['varientImage'] = img

            Varient.objects.create(product = product_, sku=sku_code, **variant)

        return product_


# Varainte ment for creation only for variants NOT Joint
class VariantOnlySerializer(serializers.ModelSerializer):
    varientImage = ImageSerialzier(required=False)
    sku = serializers.CharField(read_only=True)

    class Meta:
        model= Varient
        fields = '__all__'


    def create(self, validated_data):

        if 'varientImage' in validated_data:
            image = validated_data.pop("varientImage")
            img = Images.objects.create(**image)
            validated_data['varientImage'] = img

        variant = Varient.objects.create(**validated_data)

        return variant