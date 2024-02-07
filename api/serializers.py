from rest_framework import serializers
from .models import Locations, Custom_LocationUser
from django.contrib.auth import authenticate

from .helper import generate_location_id


#get the USER information
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_LocationUser
        fields = '__all__'
#USER LOGIN
class LoginSerializer(serializers.Serializer):
    # these are the only fileds the user will see and required to 
    username = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username').lower()
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('please provide correct email and password')
        
         
        if not Custom_LocationUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('please provide correct email or password')
       
        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            raise serializers.ValidationError('please provide correct email and password')
        
        attrs['user'] = user
        return attrs


class Update_UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model= Custom_LocationUser
        fields = ('password', 'full_name', 'position', 'is_employee')

    def update(self, attrs):
        pass


#USER SIGNUP
class CreateUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom_LocationUser
        fields = ('username', 'password', 'full_name', 'position', 'is_employee')
        extra_kwargs = {
            'password': {'required': True}
        }
    
    def validate(self, attrs):
        username = attrs.get('username', '').strip().lower()
        password = attrs.get('password').strip()

        if(len(password) < 8): # check password length
            raise serializers.ValidationError('password it to short')
        
        if Custom_LocationUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('user already exists')
        return attrs

    def create(self, validated_data):
        user = Custom_LocationUser.objects.create_user(**validated_data) # this hashed the password priveded
        return user


#get the USER information
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'

#Creating LOCATION
class CreateLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ('location_type', 'incharge', 'email', 'users', 'country',
                 'address', 'status','profit_center', 'cost_center', 'status_date')

        email = serializers.EmailField()
        
    def validate(self, attrs):
        lower_email = attrs.get('email', '').strip().lower()

        if Locations.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Duplicate")

        return attrs
    
    def create(self, validated_data):
        user = validated_data.pop('users') #removes the user from the dic and saves it to this variable
        location = Locations.objects.create(**validated_data) # create the location with all information except the user model
        location.users.set(user)
        return location
    