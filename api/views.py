from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token

from .models import Locations, LocationUsers
from .helper import generate_location_id

from .serializers import LocationsSerializer, CreateLocationsSerializer
from .serializers import UserSerializer, CreateUsersSerializer


# # Create your views here.
# CreateAPIView
class LocationView(generics.ListAPIView):
    queryset = Locations.objects.all()
    serializer_class = LocationsSerializer

# post
class CreateLocationView(APIView):

    serializer_class = CreateLocationsSerializer

    def post(self, request, format=None):
        # check users information before creating a Location
        # get the information from the form and filter the information
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            location_type = serializer.data.get('location_type')
            incharge = serializer.data.get('incharge')
            location_number = serializer.data.get('location')
            email = serializer.data.get('email')
            country = serializer.data.get('country')
            address = serializer.data.get('address')
            profit_center = serializer.data.get('profit_center')
            cost_center = serializer.data.get('cost_center')
            status = serializer.data.get('status')
            
            # if location exist Just update the information
            queryset = Locations.objects.filter(location=location_number)
            if queryset.exists():
                location = queryset[0]
                location.email = email
                location.incharge = incharge
                location.profit_center = profit_center
                location.cost_center = cost_center
                # check if the super user exist or if we need to update it
                # Save updates information
                location.save(update_fields=['email', 'incharge', 'profit_center', 'cost_center'])
                return Response({"SUCCESS":"updated"}, status=status.HTtp)

            else: # else if the location does no exist
                while True: 
                    location_id = generate_location_id(location_type, country) # this creates a location ID
                    if Locations.objects.filter(location=location_id) == 0: # checks is location exist in DB
                        break
                location = Locations(location=location_id, incharge=incharge,
                                     email=email, address=address, status=status)
                location.save()
                return Response({"SUCCESS":"created"}, status=status.HTTP_200_OK)
        else:
            return Response({"ERROR":"fields cannot be empty"}, status=status.HTTP_204_NO_CONTENT)





# this will the sign in portion of the user
class LocationUser_view(generics.ListAPIView):
    serializer_class = UserSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')

        queryset = LocationUsers.objects.filter(username=username)
        if not queryset.exists():#check if the user exist
            return Response({"ERROR":"username does not exist"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user = queryset[0]
        if not check_password(password,user.password): # check the password with the saved pasword
            return Response({"ERROR":"wrong password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # Response(UserSerializer(userLocation).data, status=status.HTTP_200_OK) 
    

    queryset = LocationUsers.objects.all()
    # Userserializer_class = UserSerializer

#logs OUT THE USER
class LogoutUser_view(APIView):
    pass   

#CREAT USER
class CreateUser_view(APIView):
    serializer_class = CreateUsersSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(): 

            username = serializer.data.get('username')
            password = serializer.data.get('password')

            # validate email

            if(len(password) < 6): # check password length
                    return Response({"ERROR: PASSWORD TO SHORT"}, status=status.HTTP_400_BAD_REQUEST)

            queryset = LocationUsers.objects.filter(username=username) # checks if theres a user with the same email

            if queryset.exists(): # You cannot create a user with the same username
                return  Response({"error":"username taken"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                name = serializer.data.get('name')
                title = serializer.data.get('title')
                superUser = serializer.data.get('superUser')
                employee = serializer.data.get('employee')
                token = Token.objects.create(user=username)
                hashed_pwd = make_password(password) # Create a hash before saving password

                userLocation = LocationUsers(username=username, password=hashed_pwd,
                                     name=name, title=title, superUser=superUser, employee=employee) # this get the information from var above and add the to the DB Model
                userLocation.save() # THIS SAVES THE INFORMATION
            return  Response({"token": token.key, "user": UserSerializer(userLocation).data}, status=status.HTTP_201_CREATED) # return response with stating user created
        else:
            return Response({"ERROR":"user not created"}, status=status.HTTP_400_BAD_REQUEST)
            
