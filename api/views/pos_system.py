from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q, F
# from decimal import Decimal
# import requests
# import os
# import environ
# import math


# from datetime import datetime, timedelta, date, time
# from dateutil import rrule
# import calendar
# import pytz

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

#MODELS
from ..models import Varient
from ..serializers import pos_serializer, varients_serializer

# functions
# from ..helper import getWompiAuthentication
from ..repeated_responses.repeated_responses import not_assiged_location, denied_permission
# from ..helper_classes.checkout import checkout_data_required, payment_data_required, checkInventory, calculate_order_amount, float_to_decimal

class CheckoutView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer = pos_serializer.SalesReceiptSerializer

    def post(self, request, format=None):
        data = request.data.copy()
        # Checking if the user is assign to a location
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()

        # TODO: make Location -> location to (lowercase)
        data['Location'] = locationID
        data['paymentExecution'] = "POS"

        # serializer serializer
        with transaction.atomic():
            salesRecieptSerializer = self.serializer(data=data)
            if salesRecieptSerializer.is_valid(raise_exception=True):
                salesRecieptSerializer.save()
            else:
                raise Exception(salesRecieptSerializer.errors)
        
        return Response(salesRecieptSerializer.data, status=status.HTTP_200_OK)



# Retrive all of the products variants as a product
class PointOfSalesProductsView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Varient.objects.all().order_by('price')
    varSerializer =  varients_serializer.retrivingProductSerialzier

    def get(self, request, format=None):
        user = request.user

        if not user.has_perm('api.view_product'):
            return denied_permission()
        
        # ALL ACTIVE 
        queryset = self.queryset.filter(product__location_id= user.location.id).filter(~Q(units__lte = 0) & Q(is_active=True))
        
        # # Retrive only varients, product name and brand
        if not queryset.exists():
            return Response({'data': []}, status=status.HTTP_200_OK)
        
        # If the user first signs in send all of the data products
        serializer = self.varSerializer(queryset, many=True) 

        return Response(serializer.data, status=status.HTTP_200_OK)











# # Get the product information
# class SKUSearch(ListAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     queryset = Varient.objects.all().order_by('price')
#     varSerializer =  varients_serializer.retrivingProductSerialzier

#     def get(self, request, format=None):  
#         user  = request.user

#         try:
#             name = request.GET.get('name')
#             sku = request.GET.get('sku')
#         except:
#             return Response({'message': 'search query required: name and sku'}, status=status.HTTP_400_BAD_REQUEST)
        
#         if sku is None:
#             sku = ''
#         if name is None:
#             name = ''

#         if not user.has_perm('api.view_product'):
#             return denied_permission()
        
#         queryset = self.queryset.filter( Q(product__name__icontains=name) & Q(sku__icontains=sku) )
        
#         # # Retrive only varients, product name and brand
#         if not queryset.exists():
#             return Response({'data': []}, status=status.HTTP_200_OK)
        
#         # If the user first signs in send all of the data products
#         serializer = self.varSerializer(queryset, many=True) 

#         return Response({'data': serializer.data }, status=status.HTTP_200_OK)
    