from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import authenticate
from drf_extra_fields.fields import Base64ImageField

from ..models import CustomUser
# from ..models import Product, Varients, VarientImages, VarientColors, ImageAlbum


#get the USER information
# TESTING ONLY
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name', 'is_active', 'avatar', 'location', 'create_on', 'groups']

#USER SIGNUP
class CreateUsersSerializer(serializers.ModelSerializer):
    # avatar = serializers.ImageField()

    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'first_name', 'location', 'avatar')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'avatar': {'required': False},
            'location': {'required': False},
        }
    
    def validate(self, attrs):
        username = attrs.get('username', '').strip().lower()
        password = attrs.get('password').strip()
        
        if(len(password) < 8):                                                                      # check password length
            raise serializers.ValidationError('password is to short')
        
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('user already exists')
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)                                     #This creates the user and hashes the password

        return user

################################ USER ####################################
##########################################################################     
#USER LOGIN
# class LoginSerializer(serializers.Serializer):

#     username = serializers.EmailField() 
#     password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

#     def validate(self, attrs):
#         username = attrs.get('username').strip().lower()
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

# update user information
class UpdateUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields = ('first_name', 'last_name', 'status_date', 'password', 'avatar')

    def update(self, instance, validated_data):
        #Check is the password exits in the validated data
        if "password" not in validated_data:
            instance = super().update(instance, validated_data)             #Update eveything that is not a password else
        else:   
            password = validated_data.pop('password')                       #pop password
            if password:
                instance.set_password(password)                             #hash and update password
            instance = super().update(instance, validated_data)             #Update eveything that is not a password else

        return instance
    