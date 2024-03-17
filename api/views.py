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
from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
import re
import os
from django.core import serializers

#this is the new session Authentication
from rest_framework import permissions
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

#### MODELS ######
from .models import Locations, CustomLocationUser
from .models import Products
from .models import Varients, ImageAlbum

##### SERIALIZERZ #####
from .serializers import LocationSerializer, CreateLocationSerializer , VarientImages#Locations
from .serializers import CreateUsersSerializer, LoginSerializer, UpdateUsersSerializer, UserSerializer #User
from .serializers import CreateProductSerializer, GetProductSerializer, UpdateProductSerializer #Products
from .serializers import CreateVarientSerializer, GetVarientSerializers, UpdatedVarientSerializer, GetImages #Varients

################################ USER ####################################
########################################################################## 
#CCREATING A USER
@method_decorator(csrf_protect, name='dispatch')
class CreateLocationUserView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CreateUsersSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            user = CustomLocationUser.objects.get(username=request.data['username']) # this catches if theirs a user in DB
            
        else:
            return  Response({"errors": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
        
        return  Response({'user': serializer.data }, status=status.HTTP_201_CREATED) # return response with stating user created
#SETS CSRF TOKEN TO USER WHEN FIRST CALLED
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'isAutheticated': 'CSRF cookie set' })
#cCHECKS USER CREDENTIALS
@method_decorator(csrf_protect, name='dispatch')
class LocationUserLoginView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request, format=None):
        try:
            if(not request.data.get("username") or not request.data.get("password")):
                return  Response({"error": {"error": ["These fields may not be blank"] } }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return  Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data.get('user')  
            login(request, user)
        else: 
            return Response({"error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
            
        return  Response({"success": "User authenticated"}, status=status.HTTP_200_OK)
#CHECK AUTHENTICATION
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })
#GET USER PROFILE
class GetUserProfileView(APIView):
    permission_classes = (AllowAny,)
    
    def get (self, request, format=None):
        try:
            user = self.request.user
            username = user.username
            print(username)

            user_profile = CustomLocationUser.objects.get(username=user)
            user_profile = UserSerializer(user_profile)

            return Response({ 'profile': user_profile.data, 'username': str(username) })
        except:
            return Response({ 'error': 'Something went wrong when retrieving profile' })
# LOGOUT USER
class LocationserLogoutView(APIView):
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return  Response({ "message": "Your are not logged in" }, status=status.HTTP_400_BAD_REQUEST)
        try: 
            logout(request)
            return  Response({ "success": "Succefully Logout" }, status=status.HTTP_200_OK)
        except:
            return  Response({ "error": "Something went Wront" }, status=status.HTTP_400_BAD_REQUEST)
# UPDATE USER INFORMATION
class UpdateUserinformationView(UpdateAPIView):
    authentication_classes = (TokenAuthentication,) #Authenticate with token
    permission_classes = (IsAuthenticated,)

    queryset = CustomLocationUser.objects.all()
    serializer_class = UpdateUsersSerializer

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

    serializer_class = CreateProductSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data, context={ 'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'succes': serializer.data}, status=status.HTTP_200_OK)

#this gets the products based on the user logged in
class GetProductsView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    
    serializer_class = GetProductSerializer

    def get_queryset(self):
        try:
            username = self.request.user
            user = CustomLocationUser.objects.filter(username=username) # filters the user
            products = Products.objects.filter(location_id=user[0].location) #we get the users Location and get all of the products that the location has
            return products
        except:
            return Response({'error': "Something went wrong retriving products"}, status=status.HTTP_200_OK)
        
#UPDATING PRODUCTS
class UpdateProductView(UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = UpdateProductSerializer
#DELETING PRODUCTS
class DeleteProductView(DestroyAPIView):
    pass


#CREATING VARIENTS
class CreateVarientView(APIView):
    # authentication_classes = (TokenAuthentication,) #This Authenticate with token
    # permission_classes = (IsAuthenticated,)

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
    
# @method_decorator(ensure_csrf_cookie, name='dispatch')
class GetVarientView(APIView):

    def get(self, request, product_id, *args, **kwargs):
        username = self.request.user   

        # product_id = request.data['product'] #TODO: FILTER THIS RESPONSE CHECK FOR BUGS

        try:
            user = CustomLocationUser.objects.get(username=username) #get the user information
        except user.DoesNotExist:
            return Response({ "error": "user doesnt exist" },status=status.HTTP_400_BAD_REQUEST)
        
        # if(not product_id):
        #     return Response({ "error": "Something went wrong" },status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Varients.objects.filter(product_id=product_id, location_id=user.location)

        if not queryset.exists():
            return Response({"error": 'products dosent have varients'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = GetVarientSerializers(queryset, many=True)
        return Response({'data': serializer.data }, status=status.HTTP_200_OK) # if nothing was found

class UpdateVarientView(UpdateAPIView):
    # authentication_classes = (TokenAuthentication,) #Authenticate with token
    # permission_classes = (IsAuthenticated,)

    queryset = Varients.objects.all()
    serializer_class = UpdatedVarientSerializer


class DeleteMultipleVarientView(RetrieveAPIView): # THIS WILL DELETE SINGLE INSTANCE
    # authentication_classes = (TokenAuthentication,) #Authenticate with token
    # permission_classes = (IsAuthenticated,)

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












    # USER LOGGIN PORTION
# class LocationUserLoginView(knox_views.LoginView):
#     permission_classes = (AllowAny,)
#     serializer_class = LoginSerializer
    
#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid(raise_exception=True):
#             user = serializer.validated_data.get('user')  
#             # VALIDATE THE THE STORE LOCATION before retriving
#             login(request, user)
#             response = super().post(request, format=None)
#             print(response)
#         else: 
#             return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
#         return  Response(response.data, status=status.HTTP_200_OK)

# UPDATE USER INFORMATION
# class UpdateUserinformationView(UpdateAPIView):
#     authentication_classes = (TokenAuthentication,) #Authenticate with token
#     permission_classes = (IsAuthenticated,)

#     queryset = CustomLocationUser.objects.all()
#     serializer_class = UpdateUsersSerializer

#CREAT USER
# class CreateLocationUserView(CreateAPIView):
#     serializer_class = CreateUsersSerializer

#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid(raise_exception=True): 
#             serializer.save()

#             user = CustomLocationUser.objects.get(username=request.data['username']) # locates the user
#             token = Token.objects.create(user=user)
#         else:
#             return  Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
#         return  Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED) # return response with stating user created

