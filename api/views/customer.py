from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..authenticate import CustomAuthentication

from datetime import datetime, timedelta, date, time
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.db.models import Q, Sum, F
from dateutil import rrule
import calendar
from django.db.models import Prefetch

from django.db.models import Sum

from ..models import Customer

from ..repeated_responses.repeated_responses import does_not_exists
from .utils import error_responses

from ..serializers import customer_serializer
# import customer proof
class customerView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # 
        user = request.user

        if not request.user.has_perm('api.add_customshipping'):
            return error_responses.permission_denied()

        # Check if the user has location before searching the phone number

        phoneNumber = request.GET.get("phone_number")

        queryset = Customer.objects.filter(phoneNumber__exact = phoneNumber)

        # print(queryset)

        # check if the user
        if not queryset.exists():
           return Response({'data': "articulo no existe."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = customer_serializer.GetCustomerSerializer(queryset[0])

         # if the user is blacklisted the return a data saying that this number is black listed
        # if queryset[0].blacklist === true:
        #     return Response({'data': {}}, status=status.HTTP_200_OK)

        # return the data or return null
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

# Search Customer by Phone Number



# Save Customer 


# 