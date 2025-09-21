from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.db import transaction
from django.db.models import Q, F, Sum, Count, Avg
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import uuid
import requests

# Models
from ..models import Varient, Product
from rest_framework.pagination import PageNumberPagination
# Serializers
from ..serializers import product_serializer
# classes
from ..helper import generate_presign_url
from ..repeated_responses.repeated_responses import not_assiged_location, emptyField, denied_permission, product_already_exist, does_not_exists, invalid_uuid
# This Creates a Product
from ..authenticate import CustomAuthentication



# get, create, update 
class ProductView(APIView):
    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    productSerializer = product_serializer.productSerializer
    # get single product
    def get(self, request, format=None):
        user = request.user

        productId = request.GET.get('product') 

        if not user.has_perm('api.view_product'):
            return denied_permission()
        # Check if the id is valid
        try: uuid.UUID(productId, version=4)     
        except: return invalid_uuid()

        if not user.location:
            return not_assiged_location()
        # This filter the product only base on the employee location
        product = Product.objects.filter(location_id = user.location, id=productId).prefetch_related("variants")
        
        if not product.exists():
            return does_not_exists()
        
        prodSerializer = self.productSerializer(product, many=True)
            
        return Response(prodSerializer.data[0], status=status.HTTP_200_OK)
    # create product
    def post(self, request, format=None):

        user = request.user
        userLocation = request.user.location.id
        # Check Permission
        if not user.has_perm('api.view_product'):
            return denied_permission()
        # Check if user has a location
        if not userLocation:
            return not_assiged_location()
        
        data = request.data.copy()

        data.update({"create_by": str(user), "location_id": userLocation })

        requiresProductInfo = ['name', 'brand', 'cost']
        # Validating if required field are present if not send error
        for pInfoReq in requiresProductInfo:
            if not pInfoReq in data:
                return emptyField()
            
        # Filtering to see if the product already exist in the data base
        cleanName = data['name'].strip().title().lstrip(",.-=/><;|")
        cleanBrand = data['brand'].strip().title().lstrip(",.-=/><;|")

        # Check if the product exists
        if Product.objects.filter(Q(name=cleanName) & Q(brand=cleanBrand)).exists():
            return product_already_exist()

        # get length of the array
        presignedUrlList = []
        # if 'varientImage' in data: 
        variants = data["variants"]
        # loop and waint for each link
        for item in variants:
            # Update each varaible with the link
            # TODO: check if the theirs a file name  before creating the links
            isImage = item.get("varientImage", None)
            if isImage:
                isFilename = isImage.get("filename", None)
                if isFilename:
                    presignedUrl = generate_presign_url()

                    if presignedUrl is None:
                        return Response({"error": "Algo salio mal suviendo las Fotos"}, status=status.HTTP_400_BAD_REQUEST)

                    presignedUrlList.append(presignedUrl["uploadURL"])
                    
                    url = settings.CLOUDFLARE_IMAGES_DOMAIN
                    account_hash = settings.CLOUDFLARE_ACCOUNT_HASH

                    signedURLID  = presignedUrl.get("id", None)
                    item["varientImage"].update({
                        "cf_id": presignedUrl["id"],
                        "link":f"{url}/{account_hash}/{signedURLID}/public"
                    })
            else:
                # delete the variant image if theirs no file name for when creating theirs no errors
                item.pop("varientImage", None)
                
        with transaction.atomic():
            serializer = self.productSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({ "data": { "message":  "Producto Creado Exitosamente",
                                    "productId": serializer.data['id'], 
                                    "upload": presignedUrlList}}, status=status.HTTP_201_CREATED)
    
    # update single product
    def patch(self, request, format=None):
        user = request.user
         # Check Permission for the user
        if not user.has_perm('api.change_product'):
            return denied_permission()
        
        # Getting the product from the query
        productId = request.GET.get('product', "")

        # check for validity of Uuid
        try: 
            uuid.UUID(productId, version=4)     
        except:
            return invalid_uuid()
                                                               
        data = request.data.copy()
        try:
            product = Product.objects.get(Q(id=productId))
        except:
            return does_not_exists()
        
        serializer = self.productSerializer(instance=product, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({"details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'details': 'Actualizado'} ,status=status.HTTP_200_OK)












#TODO: DELETE THIS VIEW
#TODO: Change to get the Inventory information like Total Products, Total Ivensted, Total Product Value
#TODO: Pass the some of the logic to the search view
class RetriveProducts(APIView, PageNumberPagination):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all().order_by('createdDate')
    productSerializer = product_serializer.productSerializer

    def get(self, request, format=None): 

        user = request.user

        if not user.has_perm('api.view_product'):
            return denied_permission()

        if not user.location:
            return not_assiged_location()
        # Filter Product
        product = Product.objects.filter(location_id = user.location).prefetch_related("variants")
        # This Aggregates the total units and total invetments
        totalUnits = product.aggregate(total_units=Sum('variants__units'))['total_units']
        totalInvesment = product.aggregate(total=Sum(F('cost') * F('variants__units')))['total']
        # This counts and get average price for each varient
        product = product.annotate(total_varients=Count('variants'), average_price=Avg("variants__price")).order_by('createdDate')

        results =  self.paginate_queryset(product, request, view=self)   
        serializer = self.productSerializer(results, many=True)

        response = self.get_paginated_response(serializer.data)
        response.data.update({ 
            'totalInvesment': totalInvesment,
            'totalVarients': totalUnits
        })
        response.data.move_to_end('results')

        return  Response({"data" : response.data}, status=status.HTTP_200_OK)


# TODO:  make search item better and more information
# TODO: This will be fitlering if it includes active and incative products
class SearchProducts(APIView, PageNumberPagination):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all().order_by('createdDate')
    Productserializer =  product_serializer.productSerializer

    def get(self, request, format=None):

        if not request.user.has_perm('api.view_product'):
            return denied_permission()

        user = request.user

        name = request.GET.get('name') 
        if name is None:
            name = '' 

        product = self.queryset.filter(location_id = user.location).filter(Q(name__icontains=name)).prefetch_related("variants")

        product = product.annotate(total_varients=Count('variants'), average_price=Avg("variants__price")).order_by('createdDate') 

        # convert to serializer
        results =  self.paginate_queryset(product, request, view=self)
        serializer = self.Productserializer(results, many=True)

        response = self.get_paginated_response(serializer.data)

        return Response(response.data, status=status.HTTP_200_OK)




# TODO: Make sure deleting products  works as intended
# TODO: Same This that the variants dele view is happeing in the product Delete View Condense code in to 1 function
#DELETING PRODUCTS
class DeleteProductView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk, *args, **kwargs):
        user = request.user

        # productId = request.GET.get('product')
        productId = pk

        if not user.has_perm('api.delete_product'):
            return denied_permission()
        
        try: 
            uuid.UUID(productId, version=4)     
        except ValueError as e:
            return invalid_uuid()
        
        product = Product.objects.filter(id=productId)
        if not product.exists():
            return does_not_exists()
        
        varients = Varient.objects.filter(product = product[0].id)

        if not varients.exists():
            return does_not_exists()
       
        try: 
            for varient in varients:
                # send the link to the 
                if(varient.varientImage):
                    if(varient.varientImage.cf_id):
                        url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/images/v1/{varient.varientImage.cf_id}"
                        headers = {"Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}"}
                        response = requests.delete(url, headers=headers)

                        # Cheking reponse of cloud flare to see if its was succesful
                        if response.status_code >= 200 and response.status_code <= 299:
                            response.raise_for_status()
                            with transaction.atomic():
                                varient.varientImage.delete()
                        else:
                            return Response({"message": 'No se puede borrar producto en este momento, Intente despues.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # Deleting Varient
                with transaction.atomic():
                    varient.delete()
            # deleting product 
            with transaction.atomic():
                product[0].delete()
        except (Exception, ValueError) as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': "Not Content"}, status=status.HTTP_204_NO_CONTENT)




# Return all products that are under a certain stock level
class LowStockLevel(ListAPIView):
    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Product.objects.all().order_by('createdDate')

    productSerializer = product_serializer.productSerializer
    paginate_by = 5

    def get(self, request, format=None):
        user = request.user

        if not user.has_perm('api.view_product'):
            return denied_permission()
        
        if not user.location:
            return not_assiged_location()
        
        # ~Q(units__lte = 0) & Q(isActive=True))
        try:            
            queryset = self.queryset.filter(variants__units__lte = F('variants__minUnits') , location_id= user.location.id, variants__isActive=True)
            serializer = self.productSerializer(queryset, many=True)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return  Response(serializer.data, status=status.HTTP_200_OK)

