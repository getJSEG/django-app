from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError, transaction
from django.db import transaction
from django.db.models import F

import re
import os
import uuid

#this is the new session Authentication
from rest_framework import permissions

#### MODELS ######
from ..models import ProductAttribute                                #product
##### SERIALIZERZ #####
from ..serializers import varients_serializer
from ..serializers import product_serializer as productSerializer

from ..helper import generate_sku

#CREATING VARIENT
class CreateVarientView(APIView):

    # Require Authentication
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        if not request.user.has_perm('api.add_varient'):
            return Response({"message": 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN) 
        try:
            # check for validity of Uuid
            uuid_obj = uuid.UUID(pk, version=4)
        except ValueError:
            return Response({"message": "product ID is not valid" },status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        print(data)
        # Spliting Data
        varient_color_data = {} # This is going to be the varient Color Data

        productAttr = ProductAttribute.objects.filter(product=pk)

        if not productAttr.exists():
            return Response({"message": "No Products was found"}, status=status.HTTP_400_BAD_REQUEST)    #checks if the varient exits
        
        # Filtering the data for the varient Color
        if 'image' in data:
            # Create the color varient 
            image  = data.pop('image')
            if not len(image) == 0:
                varient_color_data['image'] = image[0]
        # Checking Color
        if not 'color' in data:
            return Response({"message": "Color is required"}, status=status.HTTP_400_BAD_REQUEST)
        # Checking Size
        if not 'size' in data :
            return Response({"message": "Size is Required"}, status=status.HTTP_400_BAD_REQUEST)  
        # checking if theirs is a price with this varient
        if not 'price' in data: 
            data['price'] = productAttr.product.price
        
        # Generating an SKU and making is lowercase
        try: 
            sku = generate_sku(productAttr[0].product.name,
                               productAttr[0].product.brand, 
                               data["size"], 
                               data["color"], 
                               productAttr[0].product.id).lower()
        except:
            return Response({"message": "Please dont input similar data as other varients"}, status=status.HTTP_400_BAD_REQUEST) 
        
        varient_color_data['color'] = str(data.pop('color')[0]) 
        try:
            with transaction.atomic():

                # Saving Varient Color
                varientColor_serializer = varients_serializer.VarientColorSerializer(data=varient_color_data)

                if varientColor_serializer.is_valid(raise_exception=True):
                    varientColor_serializer.save()
                else:
                    return Exception(varientColor_serializer.errors)
                
                # adding the Autogenerates info to the Data dict
                data["sku"] = sku
                data['varient_color'] = varientColor_serializer.data["id"]
                data["location_id"] = productAttr[0].product.location_id.id
                # Creating Varient
                serializer = varients_serializer.CreateVarientSerializer(data=data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                else:
                    raise Exception(serializer.errors)

                varient_id = serializer.data["id"]

                productAttr[0].varients.add(varient_id) 
                productAttr[0].save()

        except IntegrityError as e:
            return Response({"message": "somthing wen wrong saving varient" },status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Varient created successfully"}, status=status.HTTP_201_CREATED)

#updating view
class UpdateVarientView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer = varients_serializer.VarientColorSerializer
    
    def patch(self, request, product, pk, *args, **kwargs):

        # Checking permissions
        if not request.user.has_perm('api.change_varient'):
            return Response({'message': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        try:
            productAttr = ProductAttribute.objects.get(product__id=product)
        except:
            return Response({"message": 'Product Was not Found'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            varient_instance = productAttr.varients.get(id=pk)
        except:
            return Response({"message": 'Varient Was not Found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if "color" in data or 'image' in data:
            # TODO: update color varient
            color_varient_serializer = varients_serializer.VarientColorSerializer(instance=varient_instance.varient_color, data=data, partial=True)
            
            if color_varient_serializer.is_valid():
                color_varient_serializer.save()
            else: 
                return Response({'error': color_varient_serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
        
        if not "color" in data: 
            color = varient_instance.varient_color.color
        else: 
            color = data["color"]

        if not "size" in data: 
            size = varient_instance.size
        else: 
            size = data["size"]

        sku = generate_sku(productAttr.product.name, productAttr.product.brand, size, color, productAttr.product.id)
        data['sku'] = sku

        #updating the varient
        varient_serializer = varients_serializer.UpdatedVarientSerializer(instance=varient_instance, data=data, partial=True)

        if varient_serializer.is_valid():
                varient_serializer.save()
        else: 
            return Response({'error': varient_serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Updated' }, status=status.HTTP_200_OK)


# TODO: Check if the varient gets deleted
class DeleteVarientView(RetrieveAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, product, pk, *args, **kwargs):
        # Check Premission for the user
        if not request.user.has_perm('api.delete_varient'):
            return Response({"message": 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN) 
        
        try:
            productAttr = ProductAttribute.objects.get(product=product)
        except:
            return Response({"message": 'Product Was not Found'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            varient = productAttr.varients.get(id=pk)
        except:
            return Response({"message": 'Product Does not have this varient'}, status=status.HTTP_400_BAD_REQUEST)
        
        varient.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# Return all products that are under a certain stock level
# No Pagination
class LowStockLevel(ListAPIView):

    queryset = ProductAttribute.objects.all().order_by('product__created_on')
    serializer_class =  productSerializer.GetProductReducedSerializer
    paginate_by = 10

    def get(self, request, format=None):
        if not request.user.has_perm('api.view_product'):
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        user = request.user

        if not user.location:
            return Response({'message': 'You are not assign to a store'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.queryset.filter(varients__units__lte = F('varients__min_units') , product__location_id= user.location.id)

        if not queryset.exists():
            return Response({'message': "Not Products Found"}, status=status.HTTP_200_OK)
        
        # results =  self.paginate_queryset(productsAttr, request, view=self)
        serializer = self.serializer_class(queryset, many=True)
        # response = self.get_paginated_response(serializer.data)

        return  Response(serializer.data, status=status.HTTP_200_OK)