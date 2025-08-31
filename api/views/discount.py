from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone
import pytz

# Permission and Authetication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..authenticate import CustomAuthentication

from ..serializers import discount_serializer

from ..models import Discount

from ..repeated_responses.repeated_responses import not_assiged_location, emptyField, denied_permission, expired, does_not_exists, already_exists

class GetDiscountView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if not request.user.has_perm('api.view_discount'):
          return denied_permission()
        # TODO: UPPER CASE THE EVRYTHING
        # TODO: REMOVE ANY COMAS, AND DOTS WHEN GETTING ND CREATING
        discount_code = request.GET.get('discount_code')
        print(discount_code)

        if discount_code and discount_code != '':
            queryset = Discount.objects.filter(discount_code__contains=discount_code)

        # print(queryset)

        if not queryset.exists():
           return does_not_exists()
        
        if queryset[0].expiration < datetime.now(tz=timezone.utc):
           return expired()
           
        serializer = discount_serializer.GetDiscountSerializer(queryset[0])
        
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


#TODO: Use Atomic WHE CREATING THIS 
class CreateDiscountView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.has_perm('api.add_discount'):
          return denied_permission()
        
        #get code
        discount_code = Discount.objects.filter(discount_code=request.data['discount'])

        if discount_code.exists():
            return already_exists()

        data = request.data.copy()
        datetime_str = data['expiration']
        datetime_object = datetime.strptime(datetime_str, '%m/%d/%y')

        data['expiration'] = datetime_object.replace(tzinfo=timezone.utc)

        serializer = discount_serializer.CreateDisocuntSerializer(data = data )

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': "success"}, status=status.HTTP_200_OK)


class DeleteDiscount(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        #permission
        if not request.user.has_perm('api.delete_discount'):
          return denied_permission()

        # id = request.GET.get('id')

        # if discount_code and discount_code != '':
        #     discount = Discount.objects.filter(discount_code__contains=discount_code)
        # else:
        discount = Discount.objects.filter(id = pk)

        if not discount.exists():
           return does_not_exists()
        
        discount.delete()
        
        return Response({'message': "No content"}, status=status.HTTP_204_NO_CONTENT)