from rest_framework import serializers

# models
from ...models import CustomUser
from django.contrib.auth.models import Group


class GroupNameField(serializers.CharField):
        def to_internal_value(self, data):
            try:
                return Group.objects.get(name=data)
            except Group.DoesNotExist:
                raise serializers.ValidationError(f"Group '{data}' does not exist.")

        def to_representation(self, value):
            return value.name
        
# this is the seriser
class userSerializer(serializers.ModelSerializer):
    # position = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    position = GroupNameField(write_only = True)
    password = serializers.CharField(write_only=True)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # username = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    # email = None
    # first_name = models.CharField(max_length=150, blank=False)
    # last_name = models.CharField(max_length=150,  null=True, blank=True)
    # password = models.CharField(max_length=255, null=False, blank=False)
    # is_staff = serializers.Boolean
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    # avatar = (required=False)

    class Meta:
        model = CustomUser
        # ('username', 'password', 'first_name', 'location', 'avatar')
        fields = '__all__'
    
    def validate(self, attrs):
        username = attrs.get('username', '').strip().lower()
        password = attrs.get('password').strip()
        
        if(len(password) < 8):                                                                      # check password length
            raise serializers.ValidationError('contraseña es muy corta')
        
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('Usuario ya Existe')
        
        return attrs
    
    def update(self, instance, validated_data):
        password  = validated_data.pop("password", None)

        if password is None:
            instance = super().update(instance, validated_data)             #Update eveything that is not a password else
        else:   
            password = validated_data.pop('password')                       #pop password
            if password:
                instance.set_password(password)                             #hash and update password
            instance = super().update(instance, validated_data)             #Update eveything that is not a password else

        return instance
    
    # creates
    def create(self, validated_data):
        position_data= validated_data.pop("position", '')
        # get the positons 
        # add the position
        
        user = CustomUser.objects.create_user(**validated_data)                                     #This creates the user and hashes the password
        user.groups.add(position_data)
        # user.groups.set(position_data)
        
        return user