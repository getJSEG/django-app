from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.exceptions import ValidationError


from django.utils import timezone

from ..models import PurchaseOrder, PurchaseOrderLines

# New Models Here DELETE ABOVE WHEN REDOING SERIALIZER
from ..models import Order, Expense, ExpenseTypes



# This Serailzer gets all of the sales from the salesReceitp
class IncomeSerialzier(serializers.ModelSerializer):
    total = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=10)

    class Meta:
        model = Order
        fields = ['totalAmount', 'dateCreated', 'total']




class ExpenseTypesSerialzer(WritableNestedModelSerializer):
    expense = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ExpenseTypes
        fields = '__all__'

# All expenses
class ExpensesSerializer(WritableNestedModelSerializer):
    expenses = ExpenseTypesSerialzer(many=True)

    class Meta:
        model = Expense
        fields = '__all__'
    
    def validate(self, data):
        expenses = data.get('expenses', None)
        totalAmount = data.get('totalAmount', None)

        expenseTotal = float(sum(expense.get('amount') for expense in expenses))
        
        if float(expenseTotal) != float(totalAmount):
            raise ValidationError("El total no coincide con las lineas de gasto")

        return data


    # def create(self, validated_data):
    #     expenseTypes = validated_data.pop('expenseType')
    #     expenseTypeIn = ExpenseTypes.objects.create(**expenseTypes)

    #     expenses = Expense.objects.create(expenseType=expenseTypeIn,**validated_data)
        
    #     return expenses

# OLD SERIALIZERS
# ["createdOn", "itemName", "sku", "unitPrice", "units", "status"]
class POLinesSerializer(WritableNestedModelSerializer):
    purchaseOrderId = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PurchaseOrderLines
        fields = '__all__'

class purchaseOrderSerializer(WritableNestedModelSerializer):
    POLines = POLinesSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def validate(self, data):
        purchaserOrderLines = data.get("POLines", None)
        totalAmount = data.get("totalAmount", None)
        status = data.get("status", None)

        if not status:
            data['status'] = 'PROCESSING'
        if totalAmount:
            POLineTotal = float(sum(purchaserOrderLine.get('subtotal') for purchaserOrderLine in purchaserOrderLines))

            if float(POLineTotal) != float(totalAmount):
                raise ValidationError("El total no coincide con las lineas de compra")

        return data
    
# class PurchseOrderDetailed(serializers.ModelSerializer):
#     purchaseOrder = POLinesSerializer(many=True)

#     class Meta:
#         model = PurchaseOrder
#         fields = ["id", "createdBy", "status", "purchaseOrder"]



# class ExpenseTypesSerialzer(serializers.ModelSerializer):

#     class Meta:
#         model = ExpenseTypes
#         fields = '__all__'

# class ExpenseSerializer(serializers.ModelSerializer):
#     expenseType = ExpenseTypesSerialzer()

#     class Meta:
#         model = Expense
#         fields = '__all__'

#     def create(self, validated_data):
#         expenseTypes = validated_data.pop('expenseType')
#         expenseTypeIn = ExpenseTypes.objects.create(**expenseTypes)

#         expenses = Expense.objects.create(expenseType=expenseTypeIn,**validated_data)
        
#         return expenses