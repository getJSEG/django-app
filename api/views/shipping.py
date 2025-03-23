from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.db import transaction

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Serializer needed
from ..serializers import pos_serializer, varients_serializer
# models
from ..models import CustomShipping, ParselShipping

from ..repeated_responses.repeated_responses import not_assiged_location

# Create custom Shipping
class RegularShippingView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    customShipppinSerializer = pos_serializer.CustomShippinSerialzier
    # Serialzier
    def post(self, request, format=None):
        # Get user location
        # Set user location where shipping is coming from
        data = request.data.copy()

        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()
        
        data['location'] = locationID
        data['shippingReceipts']["location"] = locationID
        data['shippingReceipts']["paymentExecution"] = "SHIPPING"
        
        # With Atomic HERE
        serializer = self.customShipppinSerializer(data=data)
        with transaction.atomic():
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise Exception(serializer.errors)

        # Set serializer data
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    # Updating the custom Shipping
    def patch(self, request, format=None):
        # add permission here
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()
        
        PackageId = request.GET.get("id")
        data = request.data.copy()

        try:
            package = CustomShipping.objects.filter(location=locationID).get(id=PackageId)
        except:
            return Response({"data": "Producto No Existe."}, status=status.HTTP_204_NO_CONTENT) 
        
        serializer = self.customShipppinSerializer(package, data=data, partial=True)

        with transaction.atomic():
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise Exception(serializer.errors)
        
        return Response({"message": "success"}, status=status.HTTP_200_OK) 

    # Getting all of the regular shipping 
    def get(self, request, format=None):
        # TODO: check permission here for the user

        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()
        
        status = request.GET.get('status')

        # Getting all shipping that are not closed
        shipping = CustomShipping.objects.filter(location = locationID).filter(Q(status=status))

        serializer  = self.customShipppinSerializer(shipping, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 



# Create Encomiendas
class ParselShippingView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    parselShipppinSerializer = pos_serializer.ParserShippingSerializer
    # Serialzier
    def post(self, request, format=None):
        data = request.data.copy()
        # Get user location
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()
        
        data['location'] = locationID
        data['shippingReceipts']["location"] = locationID
        data['shippingReceipts']["paymentExecution"] = "SHIPPING"
        
        # With Atomic HERE
        serializer = self.parselShipppinSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            raise Exception(serializer.errors)

        # Set serializer data
        return Response(serializer.data, status=status.HTTP_200_OK) 

    # Updating the custom Shipping
    def patch(self, request, format=None):
        # add permission here
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()
        
        PackageId = request.GET.get("id")
        data = request.data.copy()

        try:
            package = ParselShipping.objects.filter(location=locationID).get(id=PackageId)
        except:
            return Response({"data": "Producto No Existe."}, status=status.HTTP_204_NO_CONTENT) 
        
        serializer = self.parselShipppinSerializer(package, data=data, partial=True)

        with transaction.atomic():
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise Exception(serializer.errors)
        
        return Response({"message": "success"}, status=status.HTTP_200_OK) 
    




# Track ALL Shipping status, payment, closure
class TrackShippingView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    parselShipppinSerializer = pos_serializer.ParserShippingSerializer
    customShipppinSerializer = pos_serializer.CustomShippinSerialzier

    def get(self, request, format=None):

        # Track Open shipping
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()

        openParselShipping = ParselShipping.objects.filter(location = locationID).exclude(status = "PICKEDUP")
        openCustomShipping = CustomShipping.objects.filter(location = locationID).exclude(status = "DELIVERED")

        # Parsel Shipping Serializing Data
        parselSerializedData = self.parselShipppinSerializer(openParselShipping, many=True).data
        
        # Custom Shipping Serializing Data
        customShippingSerialiedData = self.customShipppinSerializer(openCustomShipping, many=True).data

        combined = {
            "parsel": parselSerializedData,
            "custom": customShippingSerialiedData
        }

        return Response(combined, status=status.HTTP_200_OK)