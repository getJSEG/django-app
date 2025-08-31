from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..authenticate import CustomAuthentication

# Models
from ..models import Varient
from ..serializers import varients_serializer
from ..serializers.Order.order_serializer import SalesReceiptSerializer

# Utils
from .utils import error_responses
"""
    Creating an order
"""
class CheckoutView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer = SalesReceiptSerializer

    def post(self, request, format=None):

        # checking the user permission
        if not request.user.has_perm('api.add_order'):
            return error_responses.permission_denied()

        data = request.data.copy()
        # Checking if the user is assign to a location
        try:
           locationID = request.user.location.id
        except:
            return error_responses.location_not_assigned()

        data['location'] = locationID
        data['paymentExecution'] = "POS"
        
        # serializer serializer
        with transaction.atomic():
            salesRecieptSerializer = self.serializer(data=data)
            if salesRecieptSerializer.is_valid(raise_exception=True):
                salesRecieptSerializer.save()
            else:
                raise Exception(salesRecieptSerializer.errors)

        print(salesRecieptSerializer.data)
        return Response(salesRecieptSerializer.data, status=status.HTTP_200_OK)



"""
    Retriving all Active variants as a product 
"""
class PointOfSalesProductsView(ListAPIView):
    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Varient.objects.all().order_by('price')
    varSerializer =  varients_serializer.retrivingProductSerialzier

    def get(self, request, format=None):

        user = request.user
        # Checking user permission is it can view products
        if not user.has_perm('api.view_product'):
            return error_responses.permission_denied()
        
        # Retriving all products that are active 
        queryset = self.queryset.filter(product__location_id= user.location.id).filter(~Q(units__lte = 0) & Q(isActive=True))
        
        # # Retrive only varients, product name and brand
        if not queryset.exists():
            return Response([], status=status.HTTP_200_OK)
        
        # If the user first signs in send all of the data products
        serializer = self.varSerializer(queryset, many=True) 

        return Response(serializer.data, status=status.HTTP_200_OK)