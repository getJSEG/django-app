from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ...authenticate import CustomAuthentication
from django.db.models import Q
from django.db import transaction
from datetime import datetime
from django.utils import timezone

# Serializer needed
# from ...serializers import pos_serializer, varients_serializer
# models
from ...models import CustomShipping, ParselShipping
from ...repeated_responses.repeated_responses import not_assiged_location
# Utils
from ..utils import error_responses
# Utils/Helper functions
from .shipping_deletion import delete_package



from ...serializers.shipping.shipping_parcel_serializer import ParserShippingSerializer
from ...serializers.shipping.shipping_custom_serializer import CustomShippinSerialzier

# This is Personal Shipping/Custom
class RegularShippingView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    customShipppinSerializer = CustomShippinSerialzier

    def get(self, request, format=None):
        # checking permission of the user
        if not request.user.has_perm('api.change_customshipping'):
            return error_responses.permission_denied()
        # add permission here
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()
        # get user information
        packageId = request.GET.get("id")
        try:
            customPackage = CustomShipping.objects.get(id=packageId, location=locationID)
        except:
            return Response({"data": "Producto No Existe."}, status=status.HTTP_204_NO_CONTENT) 

        package_data = self.customShipppinSerializer(customPackage)
        
        return Response(package_data.data, status=status.HTTP_200_OK) 
    
    
    # Creating A Product Shipment/Package
    def post(self, request, format=None):
        # checking permission of the user
        if not request.user.has_perm('api.add_customshipping'):
            return error_responses.permission_denied()

        # this is getting the data
        data = request.data.copy()

        try:
            # settign the information that is only set here in the back end
            data['location'] = request.user.location.id
            data['shippingOrder']["location"] = request.user.location.id
            data['shippingOrder']["paymentExecution"] = "SHIPPING"
        except:
            return not_assiged_location()

        # With Atomic HERE
        serializer = self.customShipppinSerializer(data=data)
        with transaction.atomic():
            with transaction.atomic():
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                else:
                    raise Exception(serializer.errors)
       
        # Set serializer data
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    # Updating the custom Shipping
    def patch(self, request, format=None):
        # checking permission of the user
        if not request.user.has_perm('api.change_customshipping'):
            return error_responses.permission_denied()
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
        # 
        serializer = self.customShipppinSerializer(package, data=data, partial=True)

        with transaction.atomic():
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise Exception(serializer.errors)
        
        return Response({"message": "success"}, status=status.HTTP_200_OK) 

    # # Getting all of the regular shipping 
    def delete(self, request, format=None):
        # checking permission of the user
        if not request.user.has_perm('api.view_customshipping'):
            return error_responses.permission_denied()
        
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()
        
        package_id = request.GET.get('package')
        package_instance = CustomShipping.objects.filter(location=locationID, id=package_id)

        if not package_instance.exists():
            return Response({"data": "Producto No Existe."}, status=status.HTTP_204_NO_CONTENT) 
        
        response = delete_package(package_instance[0], request)
        return response


















# Create Encomiendas
class ParselShippingView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    parcelShipppinSerializer = ParserShippingSerializer

    # Serialzier
    def get(self, request, format=None):
        # checking permission of the user
        if not request.user.has_perm('api.change_customshipping'):
            return error_responses.permission_denied()
        # add permission here
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()
        # get user information
        packageId = request.GET.get("id")
        try:
            parcelPackage = ParselShipping.objects.get(id=packageId, location=locationID)
        except:
            return Response({"data": "Producto No Existe."}, status=status.HTTP_204_NO_CONTENT) 

        package_data = self.parcelShipppinSerializer(parcelPackage)
        
        return Response(package_data.data, status=status.HTTP_200_OK) 
    
    def post(self, request, format=None):
        # checking permission of the user
        if not request.user.has_perm('api.add_parselshipping'):
            return error_responses.permission_denied()
        
        # making a copy of the data
        data = request.data.copy()

        try:
            data['location'] = request.user.location.id
            data['shippingOrder']["location"] = request.user.location.id
            data['shippingOrder']["paymentExecution"] = "SHIPPING"
        except:
            return not_assiged_location()
 
        # With Atomic HERE
        with transaction.atomic():
            serializer = self.parcelShipppinSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise Exception(serializer.errors)
    
        # Set serializer data
        return Response(serializer.data, status=status.HTTP_200_OK) 

    # Updating the custom Shipping
    def patch(self, request, format=None):
        if not request.user.has_perm('api.change_parselshipping'):  # checking permission of the user
            return error_responses.permission_denied()
        
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
        
        serializer = self.parcelShipppinSerializer(package, data=data, partial=True)

        with transaction.atomic():
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                raise Exception(serializer.errors)
        
        return Response({"message": "success"}, status=status.HTTP_200_OK) 
    

    def delete(self, request, format=None):
        if not request.user.has_perm('api.view_customshipping'):
            return error_responses.permission_denied()
        
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()

        package_id = request.GET.get('package', None)

        package_instance = ParselShipping.objects.filter(location=locationID, id=package_id)
        
        if not package_instance.exists():
            return Response({"detail": "Producto No Existe."}, status=status.HTTP_204_NO_CONTENT) 
        
        response = delete_package(package_instance[0], request) 
        return response




















# Track ALL Shipping status, payment, closure
class TrackShippingView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    parselShipppinSerializer = ParserShippingSerializer
    customShipppinSerializer = CustomShippinSerialzier

    def get(self, request, format=None):
        # checking permission of the user
        # this check if the user has ParselShipping and CustomShipping
        if not request.user.has_perm('api.view_parselshipping') and not request.user.has_perm('api.view_customshipping') :
            return error_responses.permission_denied()

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
    



# retrive All packages created the same date
# This gets all packeges created same day from 9am pst to 6pm pst same day
class RetriveRecentlyCreatedPackages(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    parselShipppinSerializer = ParserShippingSerializer
    customShipppinSerializer = CustomShippinSerialzier
    
    def get(self, request, format=None):

        if not request.user.has_perm('api.view_parselshipping') and not request.user.has_perm('api.view_customshipping') :
            return error_responses.permission_denied()

        # Track Open shipping
        try:
           locationID = request.user.location.id
        except:
            return not_assiged_location()


        openParselShipping = ParselShipping.objects.filter(location = locationID).filter(dateCreated__date=timezone.now()).exclude(status = "PICKEDUP")
        openCustomShipping = CustomShipping.objects.filter(location = locationID).filter(dateCreated__date=timezone.now()).exclude(status = "DELIVERED")

        # Parsel Shipping Serializing Data
        parselSerializedData = self.parselShipppinSerializer(openParselShipping, many=True).data
        

        # Custom Shipping Serializing Data
        customShippingSerialiedData = self.customShipppinSerializer(openCustomShipping, many=True).data

        combined = {
            "parsel": parselSerializedData,
            "custom": customShippingSerialiedData
        }

        return Response(combined, status=status.HTTP_200_OK)