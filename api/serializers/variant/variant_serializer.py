from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from ...models import Varient, Images, Categories, Tags, Product
# import helper
from ...helper import generate_sku

class categoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['categorie']

# def generate_sku(name, brand, size, description, productId):
#     sku = ''
#     product_id_str = str(productId)

#     try: 
#         sku = sku + name[:5].strip().title()
#         sku = sku + size[:3].strip().title()
#         words = description.split()
#         for word in  words:
#             sku = sku + word[:4].strip().title()

#         product_id = product_id_str[:8]
            
#         sku = sku +  brand[:5] + product_id
#     except: 
#         return ''

#     return ''.join(e for e in sku if e.isalnum())


class ImageSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model= Images
        fields = ["filename", "cf_id", "link"]


class variantSerializer(serializers.ModelSerializer):
    # serializers.PrimaryKeyRelatedField(read_only=True)
    sku = serializers.StringRelatedField(required=False)
    # product = ProductSerializer()
    # varientImage = ImageSerializer()
    categories = categoriesSerializer(many=True, read_only=True, required=False)
    # tags = tagsSerializer(many=True, read_only=True)

    class Meta:
        model = Varient
        fields = '__all__'

    def validate(self, data):
        color = data.get("color", None)
        size = data.get("size", None)
        product_id = data.get("product", None)

        instance = self.instance 
        # SKIP validation is we are updating
        if instance: 
            return data
        
        if color is None:
            raise ValidationError("Color Necesita ser incluido")
        if size is None:
            raise ValidationError("Tamaños necesita ser incluido")
        
        if product_id is None:
            raise ValidationError("Producto necesita ser incluido")
        else:
            sku = generate_sku(product_id.name, product_id.brand, size, color, product_id.id)
            # checks is the sku is a copy
            variant_instance = Varient.objects.filter(sku=sku)
            if variant_instance.exists():
                raise ValidationError("El ID del producto ya existe con la misma informacion, trate de cambiar la informacion")
            data["sku"] = sku

        return data

    def create(self, validated_data):
        categories = validated_data.pop("categories", None)
        tags = validated_data.pop("tags", None)
        image = validated_data.pop("varientImage", None)

        # create image here
        if image:
            img = Images.objects.create(**image)
            validated_data.update({"varientImage": img})

        # create instance here 
        variant_instance = Varient.objects.create(**validated_data)


        if categories is not None:
            categories_instances = Categories.objects.filter(categorie__in=categories)  # getting all items that are in the categories array
            if categories_instances.exists():
                # add each one to the variant inatcnce
                for obj in categories_instances:
                    variant_instance.categories.add(obj.categorie)

        if tags is not None:
            tags_instances = Tags.objects.filter(tag__in=tags) #getting all the items that exist in the tags maodel 
            if tags_instances.exists():
                # add all tags that where found to varaint inatnce
                for obj in tags_instances:
                    variant_instance.tags.add(obj.tag)

        return variant_instance


    def update(self, instance, validated_data):
        sku = validated_data.pop("sku", None) # if theirs SKU then just remove it. because we dont want the user creating their own sku
        # double check if the items i\has http inthe string if not just pop and remove the link


        # check if their is color or size in the variante then change the sku
        if("color" in validated_data or "size" in validated_data):
            size = validated_data.get('size', None)
            color = validated_data.get('color', None)
            # Change the sku
            if color is None:
                color = instance.color
            if size is None:
                size = instance.size

            instance.sku = generate_sku(instance.product.name, instance.product.brand, size, color, instance.product.id)
            instance.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance