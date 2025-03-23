from datetime import datetime
from django.utils import timezone
from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer

from rest_framework.exceptions import ValidationError
# Serialzier
from .accounting_serializer import ExpensesSerializer

# Models import
from ..models import (Varient, SalesReceipt, 
ReceiptLine, Customer, PaymentMethod, CashPayment, CreditCardPayment, TransferPayment, CustomShipping, ParselShipping)

# Helper Functions
from .SalesReceiptSerializerFunctions import updatingSalesReceipt

# Model for Cash Model
class CustomerSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# Model for Cash Model
class CashPaymentSerializer(WritableNestedModelSerializer):
    class Meta:
        model = CashPayment
        fields = '__all__'

class CreditCardPaymentSerializer(WritableNestedModelSerializer):
    class Meta:
        model = CreditCardPayment
        fields = '__all__'

class TransferPaymentSerializer(WritableNestedModelSerializer):

    class Meta:
        model = TransferPayment
        fields = '__all__'
    
# Payment Method
class PaymentMethodSerializer(WritableNestedModelSerializer):
    cashPaymentMethod = CashPaymentSerializer(required=False)
    creditcardPaymentMethod = CreditCardPaymentSerializer(required=False)
    transferPaymentMethod = TransferPaymentSerializer(required=False)

    class Meta:
        model = PaymentMethod
        fields = '__all__'
        extra_kwargs = {
            'cashPaymentMethod': {'required': False},
            'creditcardPaymentMethod': {'required': False},
            'transferPaymentMethod': {'required': False},
        }
    # This code is needed for the create functin to work????
    def to_internal_value(self, data):
        return data
    
    # Payment methos
    def create(self, validated_data):
        payment_method_type = validated_data.get('transactionType')
        relatedFields = ['cashPaymentMethod', 'creditcardPaymentMethod', 'transferPaymentMethod']

        for related in relatedFields:
            if related in validated_data:
                data = validated_data.pop(related, None)
            else:
                serializers.ValidationError("Tipo de pago invalido")
   
        payment = PaymentMethod.objects.create(**validated_data)

        if payment_method_type == 'cash':
            # Remove change due
            data.pop("transactionID", None)
            data.pop("lastDigits", None)
            CashPayment.objects.create(paymentMethod=payment, **data)
        
        elif payment_method_type == 'credit_card':
            # Remove change due
            data.pop("changeDue", None)
            CreditCardPayment.objects.create(paymentMethod=payment, **data)

        elif payment_method_type == 'bank_transfer':
            # Remove change due
            data.pop("changeDue", None)
            # Remove last digits
            data.pop("lastDigits", None)
            TransferPayment.objects.create(paymentMethod=payment, **data)
        else:
            raise serializers.ValidationError("Tipo de pago invalido")
        
        return payment

class ReceiptLineSerializer(WritableNestedModelSerializer):
    salesReceipt = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReceiptLine
        fields = '__all__'

    def validate(self, data):
        sku = data.get('sku', None)
        price = data.get('price', None)
        subtotal = data.get('subtotal', None)
        quantity = data.get('quantity', None)

        try:
            variant = Varient.objects.get(sku=sku)
        except:
            raise ValidationError("El producto no existe")
        
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
    receiptLines = ReceiptLineSerializer(many=True)
    paymentMethod = PaymentMethodSerializer()
    customer = CustomerSerializer(required=False)

    class Meta:
        model = SalesReceipt
        fields = '__all__'

    def validate(self, data):
        paymentTypes = ['cashPaymentMethod', 'creditcardPaymentMethod', 'transferPaymentMethod']
        paymentMethod = data.get("paymentMethod")
        items = data.get('receiptLines')
        grandTotal = data.get('totalAmount')
        tax = data.get("tax", None)
        discount = data.get("discount", None)
        shipping = data.get("shipping", None)
        # paymentExecution = data.get("paymentExecution", None)
        # Checking what type of payment Method
        if paymentMethod:
            for paymentType in paymentTypes:
                if paymentType in paymentMethod:
                    amountPaid = data.get("paymentMethod", None).get(paymentType, None).get("amount")
                    break

        # Getting A sum of all subtotal list items
        if items:
            sumedGrandTotal = float(sum(item.get('subtotal') for item in items))
        # Calculating Discount if theirs is Discount to calculate
        if discount:
            if float(discount) > 0:
                discountAmount = sumedGrandTotal * ( float(discount) / 100)
                sumedGrandTotal = sumedGrandTotal - discountAmount
            
        # Calculating Shipping if theirs is Shipping to calculate
        if shipping:
            if float(shipping) > 0:
                sumedGrandTotal = sumedGrandTotal + float(shipping)

        # Calculating Taxes if theirs is taxes to calculate
        if tax:
            if float(tax) > 0:
                taxAmount = sumedGrandTotal * ( float(tax) / 100)
                sumedGrandTotal = sumedGrandTotal + taxAmount
            else:
                raise ValidationError("El total no coincide con el total")
        
        # Checking if the grandTotal matches the front end if not Throw Error
        if items:
            if float(grandTotal) != float(sumedGrandTotal) :
                raise ValidationError("El total no coincide")
    
            if float(amountPaid) > float(sumedGrandTotal):
                data['status'] = "PAID"
            else:
                data['status'] = "OPEN"

        return data
    # Updating the Sales Receipt
    def update(self, instance, validated_data) :
        paymentMethodData = validated_data.pop("paymentMethod", None)
        # This is the parent of this serialzier
        # updateing all of the sales receipt items
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # get transactionType
        transType = instance.paymentMethod.transactionType

        # TODO: If item was Cancel add the shipping amount to the expenses
        # if payment Exist
        if paymentMethodData:

            updatingSalesReceipt(transType, instance, paymentMethodData, CashPaymentSerializer, TransferPaymentSerializer, CreditCardPaymentSerializer)
        return instance



# Regular Shipping
class CustomShippinSerialzier(WritableNestedModelSerializer):
    customer = CustomerSerializer()
    shippingReceipts = SalesReceiptSerializer()

    class Meta:
        model = CustomShipping
        fields = '__all__'

    def validate(self, data):
        shippingType = data.get("shippingType", None)


        if shippingType:
            if shippingType != "personalShipping":
                raise ValidationError("El tipo de envio no puede ser salvado en Paquetes Personalizados.") 

        return data
    
    # Upate all of the parent children
    def update(self, instance, validated_data):
        salesReceiptData = validated_data.pop("shippingReceipts", None)
        customerData = validated_data.pop("customer", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # if theirs customer Data and the shipping is not canceled, Updated Data Here
        if customerData and instance.status != "CANCELED":
            # Getting customer instance related to this Shipping 
            customerInstance = Customer.objects.get(id = instance.customer.id)
            # Calling serializer to update the customer models related to .this. mode
            customer_serializer = CustomerSerializer(customerInstance, data= customerData, partial=True)
            if customer_serializer.is_valid(raise_exception=True):
                customer_serializer.save()

        # If their sales Receipt data, updated here
        if salesReceiptData:
            if instance.status == "CANCELED":
                salesReceiptData["status"] = "CANCELED"
            # getting the instance of the SalesReceipt related to the parcep Model
            receitpInstance = SalesReceipt.objects.get(id=instance.shippingReceipts.id)
            # Updating the SalesReceipt if theirs items to be updated
            salesReceiptSerializer = SalesReceiptSerializer(receitpInstance, data=salesReceiptData, partial=True)
            if salesReceiptSerializer.is_valid(raise_exception=True):
                salesReceiptSerializer.save()

        return instance

# Encomienda/Parsel Shipping
class ParserShippingSerializer(WritableNestedModelSerializer):
    customer = CustomerSerializer()
    shippingReceipts = SalesReceiptSerializer()

    class Meta:
        model = ParselShipping
        fields = '__all__'

    def validate(self, data):
        shippingType = data.get("shippingType", None)

        if shippingType:
            if shippingType != "parcel":
                raise ValidationError("El tipo de envio no puede ser salvado en encomiendas.") 

        return data

    # Upate all of the parent children
    def update(self, instance, validated_data):
        salesReceiptData = validated_data.pop("shippingReceipts", None)
        customerData = validated_data.pop("customer", None)

        # Updating the information of the Shipping
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if instance.status == "CANCELED":
            salesReceiptData["shippingReceipts"]["status"] == "CANCELED"
        
        # if their customer Data, Updated Data Here
        if customerData and instance.status != "CANCELED":
            # Getting customer instance related to this Shipping 
            customerInstance = Customer.objects.get(id = instance.customer.id)
            # Calling serializer to update the customer models related to .this. mode
            customer_serializer = CustomerSerializer(customerInstance, data= customerData, partial=True)
            if customer_serializer.is_valid(raise_exception=True):
                customer_serializer.save()

        # If their sales Receipt data, updated here
        if salesReceiptData:
            if instance.status == "CANCELED":
                salesReceiptData["status"] = "CANCELED"
            # getting the instance of the SalesReceipt related to the parcep Model
            receitpInstance = SalesReceipt.objects.get(id=instance.shippingReceipts.id)
            # Updating the SalesReceipt if theirs items to be updated
            salesReceiptSerializer = SalesReceiptSerializer(receitpInstance, data=salesReceiptData, partial=True)
            if salesReceiptSerializer.is_valid(raise_exception=True):
                salesReceiptSerializer.save()

        return instance




























    # Add a success message here after its created
    # change status to closed or paid  if the amount is the same as the grand total
    # def create(self, validated_data):
    #     receiptLines = validated_data.pop("receiptLines")
    #     paymentMethodData = validated_data.pop("paymentMethod")
    #     CustomerData = validated_data.pop("customer")


    #     transactionType = PaymentMethod.objects.create(**paymentMethodData)
    #     customer = Customer.objects.create(**CustomerData)

    #     receipt = SalesReceipt.objects.create(transactionType=transactionType,customer=customer, **validated_data)

    #     # createObject
    #     for products in receiptLines:
    #         # Create
    #         ReceiptLine.objects.create(salesReceipt = receipt, **validated_data)

    #     return receipt



# class SalesOrderSerializer(serializers.ModelSerializer):

#     class Meta:
#         model= SalesOrder
#         fields = '__all__'
#         extra_kwargs = {
#             'id': {'required': False},
#         }


# # TODO: This is use to get transaction
# class TransactionReceiptSerialzier(serializers.ModelSerializer):
#     order = SalesOrderSerializer()
#     # This is for dates
#     date = serializers.CharField(read_only=True)

#     class Meta:
#         model= TransactionReceipt
#         fields = '__all__'
#         extra_kwargs = {
#             'id': {'required': False},
#         }


# class SalesOrderSerializer(serializers.ModelSerializer):

#     class Meta:
#         model= SalesOrder
#         fields = '__all__'
#         extra_kwargs = {
#             'id': {'required': False},
#         }


# class productSerial(serializers.ModelSerializer):

#     class Meta:
#         model= Product
#         fields = 'name'

# class variantSerial(serializers.ModelSerializer):
#     product = productSerial(read_only=True)
#     class Meta:
#         model= Varient
#         fields = ['product', 'size', 'color']


# class SalesOrderLineSerializer(serializers.ModelSerializer):
#     varient_id = variantSerial(read_only=True)

#     class Meta:
#         model = SalesOrderLine
#         fields = ['order_id', 'varient_id', 'price', 'qty', 'status']

#     def create(self, validated_data):
#         salesOrder = SalesOrderLine.objects.create(**validated_data)
#         return salesOrder
    

# # Getting
# class GetSalesOrderSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = SalesOrder
#         fields = '__all__'


# class TransactionReceiptSerializer(serializers.ModelSerializer):
#     # order = SalesOrderSerializer()
#     date = serializers.CharField(read_only=True)
    
    
#     class Meta:
#         model = TransactionReceipt
#         fields = '__all__'
    