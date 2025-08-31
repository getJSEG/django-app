from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from ...models import Order, ReceiptLine, Varient, Payment, CashPayment, CreditCardPayment, BankTransferPayment, CustomShipping, ParselShipping, Customer
# Serializer import 
from ..SalesReceiptSerializerFunctions import updatingSalesReceipt
from ..customer.customer_serializer import CustomerSerializer

# udpate variante after creation or updation
# sku: id the id of the product
# original qty: is the amount when first creating the object and removing it from the variant or beign added back to variant
# quantity_beign_updated: is the qty that is beign remove from 
def updateVariant(sku, original_qty, quantity_beign_updated=None):
    try:
        variant_instance  = Varient.objects.get(sku=sku)

        if(quantity_beign_updated is None):
            # get the item
            variant_instance.units = variant_instance.units - original_qty
            variant_instance.save()
        elif quantity_beign_updated is not None:
            unit_updating = variant_instance.units + original_qty
            unit_updating = unit_updating - quantity_beign_updated
            variant_instance.units  = unit_updating
            variant_instance.save()
        else:
            pass

    except ReceiptLine.DoesNotExist:
        pass

# this check the amount that was paid and changes the amount 
def check_amount_paid(grand_total, total_paid):
    status = ""
    # print("login that is beign set ",float("{:.2f}".format(float(total_paid))) >= float(grand_total))
    # print("new logic: ", float("{:.2f}".format(float(total_paid))) <= float(grand_total))
    if float("{:.2f}".format(float(total_paid))) >= float(grand_total):
        status = "PAID"
    else:
        status = "OPEN"

    return status

# Payment Method
class PaymentSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Payment

# Model for Cash Model
class CashPaymentSerializer(PaymentSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CashPayment
        fields = '__all__'

class CreditCardPaymentSerializer(PaymentSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CreditCardPayment
        fields = '__all__'

class BankTransferPaymentSerializer(PaymentSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = BankTransferPayment
        fields = '__all__'


class ReceiptLineSerializer(WritableNestedModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.IntegerField(read_only=False, required=False)

    class Meta:
        model = ReceiptLine
        fields = '__all__'

    def validate(self, data):
        id = data.get('id', None)
        sku = data.get('sku', None)
        price = data.get('price', None)
        subtotal = data.get('subtotal', None)
        quantity = data.get('quantity', None)

        try:
            variant = Varient.objects.get(sku=sku)
        except:
            raise ValidationError("El producto no existe")
        
        #######
        #removing the correct quantity bought from the inventory
        #######
        if variant.units < quantity:
            raise ValidationError("El Total de unidades es mas de la cantidad del inventario")
        
        if price:
            # Check if the price matches from the saved prices in the database
            if price != variant.price:
                raise ValidationError("Precios no coinciden con precios salvados.")
        else:
            raise ValidationError("Precio no fue incluido en el producto")
        
        if subtotal:
            # Calcualted the price of the request subtotal to the price from the database
            calculatedSubtotal = quantity * variant.price
            # If the prices dont match trow error
            if subtotal != calculatedSubtotal:
                raise ValidationError("Subtotal no coincide con nuestras calculaciones.")
        else:
            raise ValidationError("Subtotal no fue incluido en el producto")

        return data


# parent for sales Receipt
class SalesReceiptSerializer(WritableNestedModelSerializer):
    OrderLine = ReceiptLineSerializer(many=True)
    customer = CustomerSerializer(required=False)
    cashPayment = CashPaymentSerializer(required=False)
    ccPayment = CreditCardPaymentSerializer(required=False)
    btPayment = BankTransferPaymentSerializer(required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        items = data.get('OrderLine', None)
        grand_total = data.get('totalAmount')
        tax = data.get("tax", None)
        discount = data.get("discount", None)
        shipping = data.get("shipping", None)
        cash = data.get("cashPayment", None)
        cc = data.get("ccPayment", None)
        bt = data.get("btPayment", None)
        status = data.get("status", None)
        sum_grand_total = 0

        instance =  self.instance

        if cash is not None:
            amount_paid = cash.get("amount", None)
            data["status"] = check_amount_paid(grand_total, amount_paid)
        elif cc is not None:
            amount_paid = cc.get("amount", None)
            data["status"]  = check_amount_paid(grand_total, amount_paid)
        elif bt is not None:
            amount_paid = bt.get("amount", None)
            data["status"]  = check_amount_paid(grand_total, amount_paid)
        
        # Getting A sum of all subtotal list items
        if items:
            sum_grand_total = float(sum(item.get('subtotal') for item in items))
        else: 
            raise ValidationError("se necesita añadir almenos 1 prenda para crear paquete")
        # Calculating Discount if theirs is Discount to calculate
        if discount:
            if float(discount) > 0:
                discountAmount = sum_grand_total * ( float(discount) / 100)
                sum_grand_total = sum_grand_total - discountAmount
            
        # Calculating Shipping if theirs is Shipping to calculate
        if shipping:
            if float(shipping) > 0:
                sum_grand_total = sum_grand_total + float(shipping)

        # Calculating Taxes if theirs is taxes to calculate
        if tax:
            if float(tax) > 0:
                taxAmount = sum_grand_total * ( float(tax) / 100)
                sum_grand_total = sum_grand_total + taxAmount
            else:
                raise ValidationError("El total no coincide con el total")
        
        # Checking if the grandTotal matches the front end if not Throw Error
        if items:
            if float(grand_total) != float("{:.2f}".format(sum_grand_total)) :
                raise ValidationError("El total no coincide")   
        # if we are updating only do this code below
        # TODO: below is the code change the status beut i caanot chage back to the status

        if instance:
            if instance.status in ['CLOSED', 'CANCELED', 'RETURN'] and status in ['OPEN','PAID','PROCESSING']:
                raise ValidationError(f"Si el estado es {instance.status} no puedes revertirlo a{status}") 
            if instance.status in ['PAID'] and status in ['OPEN', 'PROCESSING']:
                raise ValidationError(f"Si el estado es {instance.status} no puedes revertirlo a{status}") 
            if instance.status in ['PROCESSING'] and status in ['OPEN']:
                raise ValidationError(f"Si el estado es {instance.status} no puedes revertirlo a{status}") 
           
        return data
    
    def create (self, validated_data):
        order_line_data = validated_data.pop("OrderLine", [])
        cash_payment_data = validated_data.pop("cashPayment", None)
        cc_payment_data = validated_data.pop("ccPayment", None)
        bt_payment_data = validated_data.pop("btPayment", None)
        
        # creat Order
        instance = Order.objects.create(**validated_data) 

        # create all line items & removing the quantity bough from the inventory unit
        if order_line_data:
            for line_item in order_line_data:
                ReceiptLine.objects.create(order=instance, **line_item)
                updateVariant(line_item.get("sku"), line_item.get("quantity"))
        else: 
            raise ValidationError("se necesita almeno un producto para crear la orden") 


        # create payment Method
        if cash_payment_data is not None:
            CashPayment.objects.create(order=instance, **cash_payment_data)
        elif cc_payment_data is not None:
            CreditCardPayment.objects.create(order=instance, **cc_payment_data)
        elif bt_payment_data is not None:
            BankTransferPayment.objects.create(order = instance, **bt_payment_data)
        else:
            raise ValidationError("Necesitas una forma de pago para seguir")

        return instance 
   
    # Updating the Sales Receipt
    # TODO: if the order was cancel then add the shipping to the
    def update(self, instance, validated_data):
        order_line_data = validated_data.pop("OrderLine", [])
        status = validated_data.get("status", None)

        if instance.status in ['OPEN', 'CLOSED', 'CANCELED', 'RETURN', 'PAID','PROCESSING'] and status in ['CLOSED', 'CANCELED', 'RETURN', 'PAID','PROCESSING']:
            # only update the status 
            # in ['CLOSED', 'CANCELED', 'RETURN', 'PAID','PROCESSING']
            instance.status = status
            instance.save()

        if instance.status == 'OPEN' and status == "OPEN":
        # This is the parent of this serialzier
        # check for children
            for line_item in order_line_data:
                line_item_id = line_item.get("id")
                print(line_item_id)
                # check for id
                if line_item_id:
                    # update line item
                    try:
                        order_line_instance = ReceiptLine.objects.get(id=line_item_id)
                        print(order_line_instance)
                        updateVariant(order_line_instance.sku, order_line_instance.quantity, line_item.get("quantity"))
                        ReceiptLineSerializer().update(order_line_instance, line_item)
                    except ReceiptLine.DoesNotExist:
                        pass
                else:
                    ReceiptLine.objects.create(order=instance, **line_item)
                    updateVariant(line_item.get("sku"), line_item.get("quantity"))
    

            # updating all of the sales receipt items
            # UPDATE ORDER LINE ITEM   
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()

            all_order_line_objs = instance.OrderLine.all() 
            total = 0
            for obj in all_order_line_objs:
                print("quanitty:", obj.quantity)
                total = total + obj.subtotal
            instance.totalAmount = total + instance.tax + instance.discount + instance.shipping
            instance.save()



        # Status handler here
        # if the amount paid is equal or grater that the grand total thenthe order is PAID and cannot be changed back
        # if the amount paid is 0 or less than the grand total the the status cannot be change to PAID and be left to OPEN
        # if the status is change to return or closed then the status cannot be change back
        
        # get transactionType/
        # print(instance._meta.get_fields())
        # print(paymentMethodData)
        # transType = instance.paymentMethod.transactionType

        # if payment Exist
        # if paymentMethodData:
            # updatingSalesReceipt(transType, instance, paymentMethodData, CashPaymentSerializer, BankTransferPaymentSerializer, CreditCardPaymentSerializer)

        return instance
