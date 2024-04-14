from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone
import pytz

#this is the new session Authentication
from rest_framework import permissions
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from ..serializers import discount_serializer

from ..models import Discount


class GetDiscountView(APIView):

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('api.view_discount'):
          return Response({'message': 'permission Denied'}, status=status.HTTP_401_UNAUTHORIZED)

        discount_code = request.GET.get('discount_code')

        if discount_code and discount_code != '':
            queryset = Discount.objects.filter(discount_code__contains=discount_code)

        if not queryset.exists():
           return Response({'message': "Does not Exist"}, status=status.HTTP_400_BAD_REQUEST)

        #check date
        print(queryset[0].expiration > datetime.now(tz=timezone.utc))
        
        if queryset[0].expiration < datetime.now(tz=timezone.utc):
           return Response({'message': "Discount Expired"}, status=status.HTTP_400_BAD_REQUEST)
           
        # print(discount_instance)
        
        serializer = discount_serializer.GetDiscountSerializer(queryset[0])
        
        return Response({'message': serializer.data}, status=status.HTTP_200_OK)

class CreateDiscountView(APIView):

    def post(self, request, format=None):
        if not request.user.has_perm('api.add_discount'):
          return Response({'message': 'permission Denied'}, status=status.HTTP_401_UNAUTHORIZED)
        
        #get code
        discount_code = Discount.objects.filter(discount_code=request.data['discount'])

        if discount_code.exists():
            return Response({'message': "Discount code already exist"}, status=status.HTTP_400_BAD_REQUEST)

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

    def delete(self, request, pk, format=None):
        #permission
        # if not request.user.has_perm('api.delete_discount'):
        #   return Response({'message': 'permission Denied'}, status=status.HTTP_401_UNAUTHORIZED)

        # id = request.GET.get('id')

        # if discount_code and discount_code != '':
        #     discount = Discount.objects.filter(discount_code__contains=discount_code)
        # else:
        discount = Discount.objects.filter(id = pk)

        if not discount.exists():
           return Response({'message': "Discount Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        discount.delete()
        
        return Response({'message': "No content"}, status=status.HTTP_204_NO_CONTENT)