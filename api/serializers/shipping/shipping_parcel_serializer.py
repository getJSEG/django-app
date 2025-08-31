from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError

from ...models import ParselShipping
# Serilaizer imports
from ..Order.order_serializer import SalesReceiptSerializer
from ..customer.customer_serializer import CustomerSerializer

# Encomienda/Parsel Shipping
class ParserShippingSerializer(WritableNestedModelSerializer):
    customer = CustomerSerializer()
    shippingOrder = SalesReceiptSerializer()

    class Meta:
        model = ParselShipping
        fields = '__all__'

    def validate(self, data):
        shippingType = data.get("shippingType", None)
        order = data.get("shippingOrder", None)

        if order is not None:
            order_line = order.get("OrderLine", [])
            if order_line is None or len(order_line) ==0 :
                raise ValidationError("se necesita añadir almenos 1 prenda para crear paquete") 
            
        if shippingType:
            if shippingType != "parcel":
                raise ValidationError("El tipo de envio no puede ser salvado en encomiendas.") 

        return data

    # Updating the Package
    def update(self, instance, validated_data):
        salesReceiptData = validated_data.pop("shippingOrder", None)

        # you cannot change any information if the processint
        # Rules
        # if status shipped or delivred the the only thing that can be cahnge in the order status
        # if the status is canceled or return then nothing is cahnged

        # can edit the customer information and add products
        if (instance.status == 'PROCESSING'):
            # updating the package Info
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
       
            # # checking if theirs salesReceipt data
            if salesReceiptData is not None:
                order_instance = instance.shippingOrder
                order_serliazer = SalesReceiptSerializer(instance=order_instance, data=salesReceiptData, partial=True)
                order_serliazer.is_valid(raise_exception=True)
                order_serliazer.save()
  
        else:
            raise ValidationError(f"could not update because status cannot be {instance.status}") 
        
        return instance