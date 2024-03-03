from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from knox import views as knox_views
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
import re
import os

#### MODELS ######
from .models import Locations, CustomLocationUser
from .models import Products
from .models import Varients, ImageAlbum

##### SERIALIZERZ #####
from .serializers import LocationSerializer, CreateLocationSerializer , VarientImages#Locations
from .serializers import CreateUsersSerializer, LoginSerializer, UpdateUsersSerializer #User
from .serializers import CreateProductSerializer, GetProductSerializer, UpdateProductSerializer #Products
from .serializers import CreateVarientSerializer, GetVarientSerializers, UpdatedVarientSerializer, GetImages #Varients

################################ USER ####################################
##########################################################################    
# USER LOGGIN PORTION
class LocationUserLoginView(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')  
            # VALIDATE THE THE STORE LOCATION before retriving
            login(request, user)
            response = super().post(request, format=None)
            print(response)
        else: 
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return  Response(response.data, status=status.HTTP_200_OK)

# UPDATE USER INFORMATION
class UpdateUserinformationView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,) #Authenticate with token
    permission_classes = (IsAuthenticated,)

    queryset = CustomLocationUser.objects.all()
    serializer_class = UpdateUsersSerializer

#CREAT USER
class CreateLocationUserView(CreateAPIView):
    serializer_class = CreateUsersSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True): 
            serializer.save()

            user = CustomLocationUser.objects.get(username=request.data['username']) # locates the user
            token = Token.objects.create(user=user)
        else:
            return  Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return  Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED) # return response with stating user created


################################ LOCATION ################################
##########################################################################
# this returns all of the information from ALLL locations this will not be 
class LocationView(generics.ListAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer

# CREATE LOCATION
class CreateLocationView(CreateAPIView):
    serializer_class = CreateLocationSerializer

    # TODO: CHANGE PERMISSION TO IsAdminUser

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"success": serializer.data}, status=status.HTTP_200_OK)

################################ PRODUCT ################################
##########################################################################
# this creats a product based on the user that in logged in
class CreateProductView(CreateAPIView):
    authentication_classes = (TokenAuthentication,) #This autheticates the user
    permission_classes = (IsAuthenticated,)# this is the permission

    serializer_class = CreateProductSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={ 'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Success': serializer.data}, status=status.HTTP_200_OK)

#this gets the products based on the user logged in
class GetProductsView(ListAPIView):
    authentication_classes = (TokenAuthentication,) #Authenticate with token
    permission_classes = (IsAuthenticated,)
    
    serializer_class = GetProductSerializer

    def get_queryset(self):
        username = self.request.user
        user = CustomLocationUser.objects.filter(username=username) # filters the user
        products = Products.objects.filter(location_id=user[0].location) #we get the users Location and get all of the products that the location has
        return products

class UpdateProductView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,) #Authenticate with token
    permission_classes = (IsAuthenticated,)

    queryset = Products.objects.all()
    serializer_class = UpdateProductSerializer

class DeleteProductView(DestroyAPIView):
    pass

class CreateVarientView(CreateAPIView):
    authentication_classes = (TokenAuthentication,) #This Authenticate with token
    permission_classes = (IsAuthenticated,)
    queryset = Varients.objects.all()
    serializer_class = CreateVarientSerializer

    def post(self, request, pk):

        try:
            product = Products.objects.get(id=pk) # this get the product to save it the the varient
        except product.DoesNotExist:
            return Response({"error": 'Product not found' }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data, context={ 'request': request, 'product': product})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": serializer.data }, status=status.HTTP_200_OK)

class GetVarientView(APIView):
    authentication_classes = (TokenAuthentication,) #Authenticate with token
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk, *args, **kwargs):
        username = self.request.user   
        try:
            user = CustomLocationUser.objects.get(username=username) #get the user information
        except user.DoesNotExist:
            return Response({ "error": "user doesnt exist" },status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Varients.objects.filter(product_id=pk, location_id=user.location)
        if not queryset.exists():
            return Response({"error": 'products dosent have varients'}, status=status.HTTP_400_BAD_REQUEST) # TODO: FIX THE ERROR RESPONSE ANSWER TO MAKE IT GET FROM SERIALIZER
        
        serializer = GetVarientSerializers(queryset, many=True)
        return Response({'data': serializer.data }, status=status.HTTP_200_OK) # if nothing was found

class UpdateVarientView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,) #Authenticate with token
    permission_classes = (IsAuthenticated,)

    queryset = Varients.objects.all()
    serializer_class = UpdatedVarientSerializer


class DeleteMultipleVarientView(RetrieveAPIView): # THIS WILL DELETE SINGLE INSTANCE
    authentication_classes = (TokenAuthentication,) #Authenticate with token
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        delete =  request.data['delete']
        for value in delete:
            clean_value = re.sub(r'[^a-zA-Z0-9-]',"",value)
    
            try: 
                varient_instance = Varients.objects.get(id=clean_value, product_id=kwargs['pk'])
            
                if not varient_instance.album == 'None': # when the album is None or empty
                    images = varient_instance.album.images.all()
                    for image in images:
                        os.remove(image.image.path)
                        image.delete()

                    varient_instance.album.delete()
          
                varient_instance.delete()

            except Varients.DoesNotExist:
                return Response({"error": 'Not Found'}, status=status.HTTP_400_BAD_REQUEST) 
            
        return Response({"Message": 'Not Content'}, status=status.HTTP_204_NO_CONTENT) 



#TODO: MAKE A VIEW TO Delete Images
#TODO: MAKE A VIEW TO ADD IMAGES




# class DeleteVarientView(DestroyAPIView): # THIS WILL DELETE SINGLE INSTANCE
#     authentication_classes = (TokenAuthentication,) #Authenticate with token
#     permission_classes = (IsAuthenticated,)

#     queryset = Varients.objects.all()
#     serializer_class = DeleteVarientSerializer

#     def destroy(self, request, *args, **kwargs):
#         varient_instance = self.get_object()
#         print(varient_instance)

#         return super().destroy(request, *args, **kwargs)







class GetImages(generics.ListAPIView):
    queryset = ImageAlbum.objects.all()
    serializer_class = GetImages