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
        fields = ["filename", "cf_id", "link"]

# ['id', 'color', 'size', 'units', 'minUnits', 'sku', 'price', 'tags', 'categories', 'varientImage']
class VariantSerializer(WritableNestedModelSerializer):
    varientImage = ImageSerialzier(required=False)
    # varientImage = serializers.PrimaryKeyRelatedField(read_only=True)
    sku = serializers.CharField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model= Varient
        fields = '__all__'
        optional_fields = ['varientImage' ]
        extra_kwargs = {
            "id": { "required" : False },
            "tags": { "required" : False },
            "categories": { "required" : False },
            "varientImage": { "required" : False },
            # 'sku': {'error_messages': {'unique': 'Ya Existe un variente con la misma informacion'} }
        }

    # def create(self, validated_data):
    #     # GetCategories 
    #     catergories = validated_data.pop("categories", None)
    #     # Get Tags
    #     # Create thje image
    #     print("This is in the variante serialzer: ",validated_data)

    #     variant = Varient.objects.create(**validated_data)

    #     if catergories:
    #         for category in catergories:
    #             vaari = Varient.objects.get(id=variant.id)
    #             vaari.categories.add(category)
    #             variant.save()

    #     return variant

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
        variants_data =  validated_data.pop('variants', )

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
        variants = validated_data.pop("variants", None)
        # Creating the product
        product = Product.objects.create(**validated_data)

        # if theirs variant create the product
        if variants:
            for item in variants:
                categories = item.pop("categories", None)
                tags = item.pop("tags", None)
                image = item.pop("varientImage", None)

                # creating image if theirs an image
                if image:
                    img = Images.objects.create(**image)
                    print("image Instace", img)
                    item.update({"varientImage": img})
                
                item.update({"sku": generate_sku(product.name, product.brand, item['size'], item['color'], product.id) }) 
                varInstance = Varient.objects.create(product=product, **item)

                # Add categories to Many2Many Field
                if categories:
                    for category in categories:
                        varInstance.categories.add(category)
                # Add tags to Many2Many Field
                if tags:
                    for tag in tags:
                        varInstance.tags.add(tag)

        return product