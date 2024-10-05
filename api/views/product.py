from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

#### MODELS ######
from ..models import ProductAttribute, Tags
from rest_framework.pagination import PageNumberPagination

##### SERIALIZERZ #####
from ..serializers import product_serializer 

# Uto generator or SKU and store number
from ..helper import generate_sku

import os
import uuid

# Creating Product
class CreateProductView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    product_attr = product_serializer.ProductAttributes
    product_images = product_serializer.ProductImagesSerializer

    def post(self, request, format=None):
        user = request.user
        
        if not user.has_perm('api.view_product'):
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data.copy()

        if 'name' in data or 'brand' in data or 'item_cost' in data or 'price' in data :
             Response({'message':  "Field Required" }, status=status.HTTP_400_BAD_REQUEST) 

        productAttr = {}
        product = {
            'name': data.pop('name'),
            'brand': data.pop('brand'),
            'vendor_sku': data.pop('vendor_sku') if 'vendor_sku' in data else '',
            'item_cost': data.pop('item_cost'),
            'price': data.pop('price'),
            'product_acronym': data.pop('product_acronym') if 'product_acronym' in data else '',
            'location_id': user.location.id,
            'created_by': str(user.username),
        }
        # Loop through each tags or provide and arrays of object 
        tags =  [{ 
            'tag': data.pop('tags')[0] if 'tags' in data else '' 
        }]


        productAttr['product'] = (product)
        productAttr['tags'] = tags

        with transaction.atomic():
            serializer = self.product_attr( data=productAttr)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                return Exception(serializer.errors)
            
            # Adding images one by one
            if 'images' in data:
                images = data.pop('images')
                imageData = {}

                for image in images:
    
                        imageData["images"] = image
                        imageData["album"] = serializer.instance.product.album.id

                        image_serializer = self.product_images(data = imageData)
                        if image_serializer.is_valid(raise_exception=True):
                            image_serializer.save()
                        else: 
                            return Exception(image_serializer.errors)

        return Response({'message':  "Succesfully Created" }, status=status.HTTP_201_CREATED)


# Retrives a SINGLE detailed product
class RetriveProduct(APIView,):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class =  product_serializer.GetProductAttributes

    def get(self, request, pk, format=None):
        user = request.user

        if not user.has_perm('api.view_product'):
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        if not user.location:
            return Response({'message': 'You are not assign to a store'}, status=status.HTTP_400_BAD_REQUEST)
        
        #This filter the product only base on the employee location
        productsAttr = ProductAttribute.objects.filter(product=pk, product__location_id=user.location.id) #Little infor "__" double dashed lines help seprate the information form another model fields
        
        if not productsAttr.exists():
            return Response({'message': "Product Not Found"}, status=status.HTTP_200_OK)
        
        serializer = self.serializer_class(productsAttr, many=True)
            
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

#Retrives a LIST of products with pagination
class RetriveProducts(APIView, PageNumberPagination):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = ProductAttribute.objects.all().order_by('product__created_on')
    serializer_class =  product_serializer.GetProductReducedSerializer

    def get(self, request, format=None):
        # try:
            user = request.user

            if not user.has_perm('api.view_product'):
                return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

            if not user.location:
                return Response({'message': 'You are not assign to a store'}, status=status.HTTP_400_BAD_REQUEST)

            productsAttr = self.queryset.filter(product__location_id= user.location.id) #Little infor "__" double dashed lines help seprate the information form another model fields
        
            if not productsAttr.exists():
                return Response({'message': "Not Products Found"}, status=status.HTTP_200_OK)
            
            results =  self.paginate_queryset(productsAttr, request, view=self)
            serializer = self.serializer_class(results, many=True)

            response = self.get_paginated_response(serializer.data)
            response.data['totalVarients'] = productsAttr[0].varients.through.objects.count()
            response.data['totalInvestedValue']=sum([each.product.item_cost for each in productsAttr])
            response.data.move_to_end('results')

            return  Response(response.data, status=status.HTTP_200_OK)


# Creating images
class CreateProductImagesView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        user = request.user 

        if not user.has_perm('api.add_product_images'):
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            images = request.data.pop('images')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        try:
            productAttr = ProductAttribute.objects.get(product = str(pk))
        except:
            return Response({"message": "Product Was Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(images) < 0 :
                return Response({"message": "no images"}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            imageRaw_Data = {}

            for image in images:
                imageRaw_Data["images"] = image
                imageRaw_Data["album"] = productAttr.product.album.id

                productImages_serializer = product_serializer.ProductImagesSerialzier(data = imageRaw_Data)

                if productImages_serializer.is_valid():
                    productImages_serializer.save()
                else: 
                    return Response({"error": productImages_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    
        return Response({'message':  "Succesfully Created" }, status=status.HTTP_201_CREATED)

# Deleting images
class DeleteImageProduct(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request,product, pk, format=None):
        user = request.user 

        if not user.has_perm('api.delete_product_images'):
            return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            productAttr = ProductAttribute.objects.get(product = product)
        except:
            return Response({"error": "Product Not Found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = productAttr.product_id.album.images.get(id=pk)
        except:
            return Response({"error": "Image Not Found"}, status=status.HTTP_400_BAD_REQUEST)
        
        if image.images:
            # TODO: Delete images from where ever the images are saved
            os.remove(image.images.path)
        image.delete()
        # TODO: GET THE IMAGE THAT WILL BE DELETED
        # TODO: DELETE THE IMAGES AND ITS LINK
        return Response(status=status.HTTP_204_NO_CONTENT)

#Updating Product Information
class UpdateProductView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    productSerializer = product_serializer.ProductSerializer

    def patch(self, request, pk, format=None):
        try: 
            if not request.user.has_perm('api.change_product'):
                return Response({'message': "Permissin denied"}, status=status.HTTP_403_FORBIDDEN)                # Permission for the user
            
            try:
                uuid_obj = uuid.UUID(pk, version=4)                                                               # check for validity of Uuid
            except ValueError:
                return Response({"message": "product ID is not valid" },status=status.HTTP_400_BAD_REQUEST)
            
            data = request.data.copy()

            try: 
                productAttr = ProductAttribute.objects.get(product=str(pk))
            except:
                return Response({'error': "product was not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            if 'name' in data: name = data['name']
            else: name = productAttr.product.name
            
            if 'brand' in data: brand = data["brand"]
            else: brand = productAttr.product.brand
            
            varient_array = productAttr.varients.all()

            for varient in varient_array:
                #  Update SKU
                try: 
                    sku = generate_sku(name, brand, varient.size, varient.varient_color.color, productAttr.product.id)
                except:
                    return Response({'error': 'Something went wrong when creating the SKU'}, status=status.HTTP_400_BAD_REQUEST)
                
                varient.sku = sku
                varient.save()
            serializer = self.productSerializer(instance=productAttr.product, data=data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                return Response({'message': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response({'message': "Something went wrong updating"}, status=status.HTTP_400_BAD_REQUEST)


#DELETING PRODUCTS
class DeleteProductView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, product_id, *args, **kwargs):  
        # try:
            if not request.user.has_perm('api.delete_product'):
                return Response({'message': "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                uuid_obj = uuid.UUID(product_id, version=4)                                                                 # Check for validity of uuid
            except ValueError:
                return Response({"message": "product ID is not valid" },status=status.HTTP_400_BAD_REQUEST)
            
            try:
                productAttr = ProductAttribute.objects.get(product__id=product_id)
            except:
                return Response({'message': "Product Does Not Exist"}, status=status.HTTP_400_BAD_REQUEST)

            # Delete All Images from Product
            if productAttr.product.album:
                print(productAttr.product.album.images.all())
                print(productAttr.product.album.images.remove())
                # All Images
                images = productAttr.product.album.images.all()
                for image in images:
                    if image.images:
                        print("asdasd")
                        # This is ACTUAL image Deletion
                        os.remove(image.images.path)
                    image.delete() 
                productAttr.product.album.delete()

            # Delete all varient attached to the product
            productAttr.varients.remove()
            # if productAttr.varients.exists():
            #     # this will change in the model
            #     for varient in productAttr.varient.all():
            #         if varient.varient_color:
            #             if varient.varient_color.image:
            #                 # This is ACTUAL image Deletion
            #                 os.remove(varient.varient_color.image.path)
            #         varient.delete()

            # Delete the product Attribute
            productAttr.product.delete()
            productAttr.delete()
            
            return Response({'message': "Not Content"}, status=status.HTTP_204_NO_CONTENT)
        # except:
        #     return Response({'message': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)






