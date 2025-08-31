from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError

from ...models import CustomShipping
# Serilaizer imports
from ..Order.order_serializer import SalesReceiptSerializer
from ..customer.customer_serializer import CustomerSerializer



class CustomShippinSerialzier(WritableNestedModelSerializer):
    customer = CustomerSerializer()
    shippingOrder = SalesReceiptSerializer()

    class Meta:
        model = CustomShipping
        fields = '__all__'

    def validate(self, data):
        shippingType = data.get("shippingType", None)
        status =  data.get("status", None)

        instance = self.instance

        if shippingType:
            if shippingType != "personalShipping":
                raise ValidationError("El tipo de envio no puede ser salvado en Paquetes Personalizados.") 
        if instance: 
            if instance.status in ['CANCELED', 'RETURN'] and status in["PROCESSING","SHIPPED", "DELIVERED"]:
                raise ValidationError(f"Si el estado es {instance.status} no puedes revertirlo a {status}") 
            
            if instance.status in ['SHIPPED', 'DELIVERED'] and status in["PROCESSING"]:
                raise ValidationError(f"El Estado no se puedes revertirlo a procesando") 
            
            if instance.status in ['DELIVERED'] and status in["SHIPPED"]:
                raise ValidationError(f"El Estado no se puedes revertirlo a Enviado") 
            

        return data
    
    # Upate all of the parent children
    def update(self, instance, validated_data):
        salesReceiptData = validated_data.pop("shippingOrder", None)
        status = validated_data.get('status', None)
        shipping_status = ["PROCESSING","SHIPPED", "DELIVERED", "RETURN","CANCELED"]

        if instance.status in ["PROCESSING","SHIPPED", "DELIVERED", "RETURN","CANCELED"] and status in ["SHIPPED", "DELIVERED", "RETURN", "CANCELED"]: 
            # update items in the status and or orde
            instance.status = status
            instance.save()
            if salesReceiptData is not None:
                order_instance = instance.shippingOrder
                order_serliazer = SalesReceiptSerializer(instance=order_instance, data=salesReceiptData, partial=True)
                order_serliazer.is_valid(raise_exception=True)
                order_serliazer.save()
        
        elif instance.status == 'PROCESSING' and status == "PROCESSING" :
            # updating the package Info
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
       
            # checking if theirs salesReceipt data
            if salesReceiptData is not None:
                order_instance = instance.shippingOrder
                order_serliazer = SalesReceiptSerializer(instance=order_instance, data=salesReceiptData, partial=True)
                order_serliazer.is_valid(raise_exception=True)
                order_serliazer.save()
        else:
            raise ValidationError("No se puede cambiar si el estado no es Procesando") 
        
        return instance