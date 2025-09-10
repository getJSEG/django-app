from rest_framework import serializers
from ...models import Location



# Main Location Serizer
class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        fields = '__all__'
        extra_kwargs = {
            "tax": { "required" : False },
            "isPreTax": { "required" : False }, 
            "email": { "required" : False },
            "phone": { "required" : False }, 
            "currency": { "required": False }
        }

        email = serializers.EmailField()
        
    def validate(self, attrs):
        lower_email = attrs.get('email', '').strip().lower()
        incharge = attrs.get('incharge', '').title()
        address = attrs.get('address', '').title()
        department = attrs.get('department', '').title()
        city = attrs.get('city', '').title()
        country = attrs.get('country', '').title()
        location_type = attrs.get('locationType', '').title()
        status = attrs.get('status', '').strip().title()

        # if Locations.objects.filter(email__iexact=lower_email).exists():
        #     raise serializers.ValidationError("Duplicate")
        
        attrs['incharge'] = incharge 
        attrs['address'] = address
        attrs['city'] = city
        attrs['department'] = department
        attrs['country'] = country
        attrs['locationType'] = location_type
        attrs['status'] = status
        attrs['email'] = lower_email

        return attrs