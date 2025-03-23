
from django.utils import timezone

from  .accounting_serializer import ExpensesSerializer
from ..models import CashPayment, TransferPayment, CreditCardPayment
from rest_framework.exceptions import ValidationError


def addExpenses(instance):
    shippingPrice = instance.shipping or 3.99
    expenseData = {
        "totalAmount": shippingPrice ,
        "location": instance.location.id,
        "created_by": "System",
        "expenses": [{
            "amount": shippingPrice,
            "description": "Canceled Shipping",
            "approvalDate": timezone.datetime.now(),
            "expense_date": timezone.datetime.now(),
            "expense_type": "Shipping was cancel"
        }]
    }
    expense_Serializer = ExpensesSerializer(data=expenseData)
    if expense_Serializer.is_valid(raise_exception=True):
        expense_Serializer.save()
    else:
        raise Exception(expense_Serializer.errors)


def updatingSalesReceipt(transType, instance, paymentMethodData, CashPaymentSerializer, TransferPaymentSerializer, CreditCardPaymentSerializer):
        if transType == "cash":
            if instance.status == "PAID":
                try:
                    paymentMethodData["cashPaymentMethod"]["amount"] = instance.totalAmount
                except:
                    raise ValidationError("Algo salio mal en nuestro sistema: codigo 1700")
            elif instance.status == "CANCELED":
                # This function adds the shipping expense if the status is "canceled"
                addExpenses(instance)
                try:
                    paymentMethodData["cashPaymentMethod"]["amount"] = paymentMethodData["cashPaymentMethod"]["amount"] or 0
                except:
                    raise ValidationError("Algo salio mal en nuestro sistema: codigo 1702")
            else:
                try:
                    paymentMethodData["cashPaymentMethod"]["amount"] = paymentMethodData["cashPaymentMethod"]["amount"]
                except:
                    raise ValidationError("Algo salio mal en nuestro sistema: codigo 1703")

            objectInstance = CashPayment.objects.get(paymentMethod=instance.paymentMethod.id)
            paymentTypeSerializer = CashPaymentSerializer(objectInstance, data=paymentMethodData.get("cashPaymentMethod"), partial=True)
        # Find the object in the cc model
        if transType == "credit_card":
            if transType == "credit_card":
                if instance.status == "PAID":
                    try:
                        paymentMethodData["creditcardPaymentMethod"]["amount"] = instance.totalAmount
                    except:
                       raise ValidationError("Algo salio mal en nuestro sistema: codigo 1800")
                elif instance.status == "CANCELED":
                    # This function adds the shipping expense if the status is "canceled"
                    addExpenses(instance)
                    try:
                        paymentMethodData["creditcardPaymentMethod"]["amount"] = paymentMethodData["creditcardPaymentMethod"]["amount"] or 0
                    except:
                       raise ValidationError("Algo salio mal en nuestro sistema: codigo 1801")
                else:
                    try:
                        paymentMethodData["creditcardPaymentMethod"]["amount"] = paymentMethodData["creditcardPaymentMethod"]["amount"]
                    except:
                       raise ValidationError("Algo salio mal en nuestro sistema: codigo 1803")
            
            objectInstance = CreditCardPayment.objects.get(paymentMethod=instance.paymentMethod.id)
            paymentTypeSerializer = CreditCardPaymentSerializer(objectInstance, data=paymentMethodData.get("creditcardPaymentMethod"), partial=True)

        # Find the object in the Transfer Model
        if transType == "bank_transfer":
            if transType == "bank_transfer":
                if instance.status == "PAID":
                    try:
                        paymentMethodData["transferPaymentMethod"]["amount"] = instance.totalAmount
                    except:
                       raise ValidationError("Algo salio mal en nuestro sistema: codigo 1900")
            
                elif instance.status == "CANCELED":
                    # This function adds the shipping expense if the status is "canceled"
                    addExpenses(instance)
                    try:
                        paymentMethodData["transferPaymentMethod"]["amount"] = paymentMethodData["transferPaymentMethod"]["amount"] or 0
                    except:
                       raise ValidationError("Algo salio mal en nuestro sistema: codigo 1901")
                else:
                    try:
                        paymentMethodData["transferPaymentMethod"]["amount"] = paymentMethodData["transferPaymentMethod"]["amount"]
                    except:
                       raise ValidationError("Algo salio mal en nuestro sistema: codigo 1903")
            objectInstance = TransferPayment.objects.get(paymentMethod=instance.paymentMethod.id)
            paymentTypeSerializer = TransferPaymentSerializer(objectInstance, data=paymentMethodData.get("transferPaymentMethod"), partial=True)

        if paymentTypeSerializer.is_valid(raise_exception=True):
            paymentTypeSerializer.save()