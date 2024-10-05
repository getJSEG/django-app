from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction


from datetime import datetime, timedelta, date, time
from dateutil import rrule
import calendar
import pytz

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

#MODELS
from ..models import ProductAttribute, Varient, SalesOrder

from ..serializers import pos_serializer, product_serializer

# Get the product information
class SKUSearch( APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # add extra protection for this request
    def get(self, request, format=None):
                
        user  = request.user
        # TODO: check if they are able to view the information
        if not user.has_perm('api.view_varient'):
            return Response({"message": 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)   
        
        # This mign need an TRY  except
        sku = request.GET.get('sku', "")

        print(sku)

        # search for the product and the search for the varient 
        try:
            productAttr = ProductAttribute.objects.get(varients__sku = sku)
        except:
            return Response({'message': 'varient Not Found'}, status=status.HTTP_400_BAD_REQUEST)

        print(productAttr.product.name)
        # TODO: Change this from Filter to Get
        varient = productAttr.varients.filter(sku=sku)

        # TODO: apply error checking 
        return Response({'data': 
                         {  'name': productAttr.product.name,
                            'price': varient[0].price,
                            'sku': varient[0].sku,
                            'currency': 'USD',
                            'size':  varient[0].size,
                            'color': varient[0].varient_color.color,
                         }
                        }, status=status.HTTP_200_OK)

# TODO: Protect this route with login and permissions
# TODO: After each an final sales create an AccountReceivables to store all of the revenue
# TODO: ADD A is_paid = True
class checkout(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def  post(self, request, format=None):

        data = request.data.copy()
        try:
            payment_type =  str(data.pop('payment_type')).upper()
        except:
            return Response({'error': 'Need payment type'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # This will be deleted and replaced with the user location
            location = request.data.pop('location_id')
        except:
            return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        # getting the total
        try:
            grand_total = request.data.pop('order_total_price')
            amount_paid = request.data.pop('order_total_paid')
        except:
            return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            items = data.pop('items')
        except:
            return Response({"message": 'No items found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(items) <= 0:
            return Response({"message": 'No Products'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Use transactions
        data['created_by'] = str(request.user)
        item_list = []

        try: 
            with transaction.atomic():
                #Create Sales Order
                data['status'] = 'PAID'
                salesOrder_serializer = pos_serializer.SalesOrderSerializer(data=data)

                if salesOrder_serializer.is_valid():
                    salesOrder_serializer.save()
                else:
                    raise Exception(salesOrder_serializer.errors)

                salesOrder_id = salesOrder_serializer.data['id']

                # check is its cash or credit card
                if "CASH"  or 'TRANSFER' in payment_type:
                    transaction_data = {}

                    transaction_data['location_id'] = location
                    transaction_data['order'] = salesOrder_id
                    transaction_data["amount_received"] = amount_paid
                    transaction_data['amount'] = grand_total
                    transaction_data['order_total'] = grand_total
                    transaction_data['refundable_amount'] = grand_total
                    transaction_data['transaction_type'] = payment_type
                    #Creating a transaction receipt
                    TransactionReceipt_serializer = pos_serializer.TransactionReceiptSerializer(data=transaction_data)
                    if TransactionReceipt_serializer.is_valid():
                        TransactionReceipt_serializer.save()
                    else:
                        raise Exception(TransactionReceipt_serializer.errors)

                elif 'CREDIT' or 'DEBIT' in payment_type:
                    # rename this cc offline
                    #cc Athorization is needed to complete transaction
                    print('payment type is Credit card')

                # Create a salesorderList for each item bought 
                for item in items:
                    item['order_id'] = salesOrder_id
                    item['quantity'] = item['unit']
                    item['status'] = 'CLOSED'

                    # remove the units bought from the inventory
                    varient_intance = Varient.objects.get(sku= item["sku"])
                    # throw a exception error
                    if varient_intance.units < item['unit']:
                        raise Exception("Not enough items in stock")
                    
                    varient_intance.units -= item['unit']
                    varient_intance.save()

                    item["varient_id"] = varient_intance.id
                    salesOrderLine_serializer = pos_serializer.SalesOrderLineSerializer(data = item)
                    if salesOrderLine_serializer.is_valid():
                        salesOrderLine_serializer.save()
                    else:
                        raise Exception(salesOrderLine_serializer.errors)
                    
                    item_list.append(salesOrderLine_serializer.data)
        except Exception as e:
            return Response({"message": str(e) }, status=status.HTTP_400_BAD_REQUEST)

        # TODO: CHENGE THIS TO GET MULTPLE ITEMS
        receipt = {}
        receipt["items"] = item_list
        receipt["Order"] = salesOrder_serializer.data
        receipt['transaction'] = TransactionReceipt_serializer.data

        print(receipt)
        return Response({'data': receipt }, status=status.HTTP_200_OK)


# This get all of the sales Order from that week
class SalesorderView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class =  pos_serializer.GetSalesOrderSerializer

    def  get(self, request, format=None):

        date = datetime.now()
        start_week =  date - timedelta(date.weekday())
        end_week = start_week + timedelta(7)

        try:
            location =  request.user.location.id
        except:
            return Response({'data': "you are not assign to a location" }, status=status.HTTP_400_BAD_REQUEST)


        # This will be change 
        # the the actial full Week 
        # star of the week -> until todays date

        salesOrder_instance = SalesOrder.objects.filter(location_id = location, date_created__date__range=[start_week, end_week])

        serializer = self.serializer_class(salesOrder_instance, many=True)
        return Response({'data': serializer.data }, status=status.HTTP_200_OK)



class RetriveVarientsProducts(ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ProductAttribute.objects.all().order_by('product__created_on')
    serializer_class =  product_serializer.getProductAttributePOSSerializer

    def get(self, request, format=None):

        user = request.user

        if not user.has_perm('api.view_product'):
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.queryset.filter(product__location_id= user.location.id)
        
        # Retrive only varients, product name and brand
        if not queryset.exists():
            return Response({'message': "Not Products Found"}, status=status.HTTP_200_OK)
        
        # If the user first signs in send all of the data products
        serializer = self.serializer_class(queryset, many=True)
        # Else retrive all of the products that 

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)