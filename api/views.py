from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from knox import views as knox_views
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.contrib.auth import login

from .models import Locations, Custom_LocationUser
# from .helper import generate_location_id

from .serializers import LocationSerializer, CreateLocationSerializer
from .serializers import CreateUsersSerializer, LoginSerializer

# SIGN IN PORTION
class LoginUser_view(knox_views.LoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')  
            login(request, user)
            response = super().post(request, format=None)
        else: 
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return  Response(response.data, status=status.HTTP_200_OK)


#UPDATE USER
class LogoutUser_view(APIView):
    pass   

#CREAT USER
class CreateUser_view(CreateAPIView):
    serializer_class = CreateUsersSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True): 
            serializer.save()

            user = Custom_LocationUser.objects.get(username=request.data['username']) # locates the user
            token = Token.objects.create(user=user)
        else:
            return  Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return  Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED) # return response with stating user created

class LocationView(generics.ListAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationSerializer



# CREATE LOCATION
class CreateLocationView(CreateAPIView):
    serializer_class = CreateLocationSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            # location_type = serializer.data.get('location_type').lower()
            # country = serializer.data.get('country')
            # location_id = ''    
            
            # #  Auto create location ID 
            # while True: 
            #     location_id = generate_location_id(request.data('location_type'), request.data('country')) # this creates a location ID
            #     if not Locations.objects.filter(location=location_id).exists(): # checks is location exist in DB
            #         break

        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"sucess": serializer.data}, status=status.HTTP_200_OK)





