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
from .helper import generate_location_id

from .serializers import LocationsSerializer, CreateLocationsSerializer
from .serializers import UserSerializer, CreateUsersSerializer, LoginSerializer


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





# SIGN IN PORTION
class LocationUser_view(knox_views.LoginView):
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


#logs OUT THE USER
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

        
            
