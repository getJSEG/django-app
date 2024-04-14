from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone

#MODELS
from ..models import Varients, VarientImages, VarientColors, ImageAlbum 
from ..models import SalesOrderLines, SalesOrder, PaymentVoucher, Discount

from ..serializers import point_of_sales_serializer as posSerealizer

from ..helper import cal_balance

#this will get the item from the DB
class SKUSearch(APIView):
    def get(self, request, format=None):
                
        user  = request.user

        if not user.has_perm('api.view_varients'):
            return Response({"message": 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)   

        sku = request.data['sku']

        print(sku)

        try:
            product = Varients.objects.get(sku=sku)
        except:
            return Response({'message': 'SKU was not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        product_validated = posSerealizer.GetVarient(product)

        return Response({'message': product_validated.data }, status=status.HTTP_200_OK)


class POSTransaction(APIView):

    def post(self, request, format=None):
        
        user = request.user

        if not user.groups.filter(name__in=['Manager', 'Employee']).exists() :
            return Response({"message": 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN) 
        
        if not user.has_perm('api.add_invoice'):
            return Response({"message": 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)   

        data = request.data
        local_tax = user.location.local_tax
        profit_center = 'Clothing'
        order_type = 'RETAIL'  
        subtotal = 0
        total_taxes = 0
        grand_total = 0      
        discount_perc= 0
        
        if 'discount' in request.data:
            discount_code = request.data["discount"]
            discount_instance = Discount.objects.filter(discount_code=discount_code)

            if discount_instance.exists():
                if discount_instance[0].expiration < datetime.now(tz=timezone.utc):
                    discount_perc = 0
                else:
                    discount_perc = discount_instance[0].discount

        

        payment = request.data.pop("payment")
        amount_paid = int(float(request.data.pop("amount paid")))

        if payment == "CREDIT" or payment == "DEBIT":
            if not 'cc_authcode' in request.data:
                return Response({'message': "Provide Authorization Code for the Credit card or Debit card payment" }, status=status.HTTP_400_BAD_REQUEST)

        # This Creates a Sales Order
        salesOrder_dict = {
            "location_id": user.location,
            "profit_center": profit_center,
            "order_type": order_type,
            "status_date": datetime.now(tz=timezone.utc)
        }
        sales_order = SalesOrder.objects.create(**salesOrder_dict)                                      #creating Sales Order
        
        #this create line item for every product that was scanned
        for info in data:
            try: 
               varient = Varients.objects.get(sku=data[info]["sku"])                                     #this gets the items from the models by the sku
            except:
                pass
            
            if 'sku' in data[info]:
                sku_temp = data[info]['sku']
            if 'quantity' in data[info]:
                qty_temp = data[info]['quantity']

            salesOrderLine_dict = {                                                                      # this calculates the quantity and the price to calculate the subtotal
                "location_id": user.location,
                "order_id": sales_order,
                "varient_id": varient,
                "sku": sku_temp,
                "item_name": varient.name,
                "unit_price": int(float(varient.listed_price)),
                "quantity": qty_temp,
                "total_price": int(float(varient.listed_price * qty_temp)),
                "status_date": datetime.now(tz=timezone.utc)
            }

            subtotal = subtotal + salesOrderLine_dict["total_price"]                                    #This adds up all of the line items sub total                                  
            SalesOrderLines.objects.create(**salesOrderLine_dict)                                       #this create line items

        if not user.location.pre_tax_items == True:
            tax_rate = local_tax / 100
            total_taxes = (subtotal * tax_rate)

        # if dicount if above 0 percent
        if discount_perc > 0:
            discount_to_dec = discount_perc / 100
            discount_in_dollars = subtotal * discount_to_dec

            print(discount_in_dollars)

            subtotal = subtotal - discount_in_dollars

        grand_total = subtotal + total_taxes
        balance = int(float(cal_balance(grand_total, amount_paid)))

        #TODO: Convert everything to USD before doing any math
        if balance > int(float(0.00)):
            return Response({'message': "Payment Needed" }, status=status.HTTP_400_BAD_REQUEST)
        
        invoice_data = {
            "location_id": user.location.id,
            "sales_order_id": sales_order.id,
            "subtotal": int(float(subtotal)),
            "total_tax": int(float(total_taxes)),
            "grand_total": int(float(grand_total)),
            "discount": discount_perc,
            "amount_paid": int(float(amount_paid)),
            "change":int(float(balance)),
            "payment_type": payment,
            "created_by": user.username,
            "status": "paid"
        }
        serializer = posSerealizer.CreateInvoiceSerializer(data=invoice_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({'message': serializer.data }, status=status.HTTP_200_OK)
