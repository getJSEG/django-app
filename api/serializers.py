# from datetime import datetime
from rest_framework import serializers
# from django.contrib.auth import authenticate
# from drf_extra_fields.fields import Base64ImageField

# from .models import Locations
from .models import CustomUser
# from .models import Products, Varients, VarientImages, VarientColors, ImageAlbum


# #get the USER information
# # TESTING ONLY
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'

# #USER SIGNUP
# class CreateUsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'password', 'first_name' 'location', 'avatar')
#         extra_kwargs = {
#             'password': {'required': True}
#         }
    
#     def validate(self, attrs):
#         username = attrs.get('username', '').strip().lower()
#         password = attrs.get('password').strip()
#         #TODO: GET THE USER AND RESIZE THE IMAGE BEFORE STORING TO DATABASE
#         if(len(password) < 8): # check password length
#             raise serializers.ValidationError('password it to short')
        
#         if CustomUser.objects.filter(username=username).exists():
#             raise serializers.ValidationError('user already exists')
#         return attrs

#     def create(self, validated_data):
#         # avatar_validated = validated_data.pop('avatar')
#         user = CustomUser.objects.create_user(**validated_data) # this hashed the password provided

#         # user.locations.set(location)
#         return user

# ################################ USER ####################################
# ##########################################################################     
# #USER LOGIN
# class LoginSerializer(serializers.Serializer):
#     # these are the only fileds the user will see and required to 
#     username = serializers.EmailField()
#     password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

#     def validate(self, attrs):
#         username = attrs.get('username').lower()
#         password = attrs.get('password')

#         if not username or not password: # check is password and username are not empty
#             raise serializers.ValidationError('please provide email and password')
           
#         if not CustomUser.objects.filter(username=username).exists(): # check if the user exist
#             raise serializers.ValidationError('wrong Email or Password')
 
#         user = authenticate(request=self.context.get('request'), username=username, password=password)
        
#         if not user: # throw error if information does not match
#             raise serializers.ValidationError('wrong Email or Password')

#         attrs['user'] = user
#         return attrs

# # update user information
# class UpdateUsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= CustomUser
#         fields = ('first_name', 'last_name', 'position', 'is_employee', 'status_date', 'password', 'avatar')

#     def update(self, instance, validated_data):
#         password = validated_data.pop('password')
#         if password:
#             instance.set_password(password)
#         instance = super().update(instance, validated_data)
#         return instance
    
# ################################ LOCATION ################################
# ##########################################################################
# # TESTING ONLY
# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Locations
#         fields = '__all__'

# #Creating LOCATION
# #MODIFI 
# class CreateLocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Locations
#         fields = ('location_type', 'incharge', 'email', 'country',
#                  'address', 'status','profit_center', 'cost_center', 'status_date')

#         email = serializers.EmailField()
        
#     def validate(self, attrs):
#         lower_email = attrs.get('email', '').strip().lower()

#         if Locations.objects.filter(email__iexact=lower_email).exists():
#             raise serializers.ValidationError("Duplicate")

#         return attrs
    
# ################################ PRODCUTS ####################################
# ##############################################################################
# class ProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= Products
#         fields = '__all__'

# # ################################ PRODUCT ################################
# # #########################################################################
# # class CreateProductSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Products
# #         fields = ('name', 'brand')
    
# #     def validate(self, attrs):
# #         user = self.context['request'].user

# #         get_user = CustomUser.objects.filter(username=user)
        
# #         if not get_user.exists():
# #             raise serializers.ValidationError("user not found") 
# #         return attrs
        
# #     def create(self, validated_data):
# #         username = self.context['request'].user
# #         user = CustomUser.objects.filter(username=username)
# #         product = Products.objects.create(**validated_data, location_id=user[0].location)
# #         return product

# # class GetProductSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Products
# #         fields = '__all__'

# # class UpdateProductSerializer(serializers.ModelSerializer):
# #     class Meta: 
# #         model = Products
# #         fields = ['name', 'brand', 'product_acronym']

# #     def update(self, instance, validated_data):
# #         instance.status_date = datetime.now() 
# #         instance = super().update(instance, validated_data)
# #         return instance

# ################################ VARIENTS ################################
# ##################################################################################
# #IMAGE
# # class VarientImageSerializer(serializers.ModelSerializer):
# #     # image = Base64ImageField(required=False) # Base64ImageField
# #     image = serializers.ImageField()
    
# #     class Meta:
# #         model = VarientImages
# #         fields = ['image']
    
# #     def create(self, validated_data, album):
# #         varient_img = VarientImages.objects.create(image=validated_data, album=album)
# #         return varient_img
# # #ALBUM
# # class AlbumSerializer(serializers.ModelSerializer):
# #     images = VarientImageSerializer(many=True)

# #     class Meta:
# #         model = ImageAlbum
# #         fields = ['images']

# #     def create(self, validated_data):
# #         images = validated_data
# #         album = ImageAlbum.objects.create()

# #         for image in images:
# #             varientImage = VarientImageSerializer.create(VarientImageSerializer(), image, album)

# #         album.images.add(varientImage)
# #         return album
    
# #     def update(self, instance, validated_data):
        
# #         images = validated_data.pop('images')

# #         for image in images:
# #             varientImage = VarientImageSerializer.create(VarientImageSerializer(), image, instance)

# #         instance.images.add(varientImage)
# #         return super().update(instance, validated_data)
    

# # #VARIENT
# # class CreateVarientSerializer(serializers.ModelSerializer):

# #     class Meta:
# #         model = Varients
# #         fields = ['name', 'size', 'units', 'purchase_price', 'list_price', 'album']

# #     def validate(self, attrs):
# #         print(attrs)
# #         return attrs

# #     def create(self, validated_data):
# #         user = self.context['request'].user
# #         product = self.context['product']

# #         product_varient = Varients.objects.create(**validated_data, product_id=product, location_id=user.location) # creating produc

# #         return product_varient





# # class GetVarientSerializers(serializers.ModelSerializer):
# #     album = AlbumSerializer()
# #     price = serializers.IntegerField(source='cal_purchase_price')

# #     class Meta:
# #         model = Varients
# #         fields = '__all__'
# #         read_only_fields = ['id', 'name', 'size', 'units', 'sku', 'album','price']



# # class UpdatedVarientSerializer(serializers.ModelSerializer):
# #     album = AlbumSerializer()

# #     class Meta:
# #         model = Varients
# #         fields = ['name', 'units', 'size', 'album']

# #     def update(self, instance, validated_data):
# #         data = validated_data.pop('album')

# #         album_re = AlbumSerializer.update(self=AlbumSerializer(), instance=instance.album, validated_data=data)

# #         instance = super().update(instance, validated_data)
# #         return instance


# # #TESTING
# class GetImages(serializers.ModelSerializer):
#     # album = sampleAlbumSerializer()
#     class Meta:
#         model = ImageAlbum
#         fields = ['id']
#         # related_fields=['album']






