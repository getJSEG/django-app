from drf_writable_nested.serializers import WritableNestedModelSerializer
from ...models import ParselShipping, Customer


class CustomerSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'