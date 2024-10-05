from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _
from django.db import transaction

from rest_framework import status
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.tokens import RefreshToken


#### MODELS ######
from ..models import CustomUser

##### SERIALIZERZ #####
from ..serializers import user_serializers as user_ser

# TODO: REGISTER
class CreateEmployeeView(RegisterView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = user_ser.CreateUsersSerializer

    def post(self, request, format=None):

        if not request.user.has_perm('api.add_customuser'):
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
        data = request.data
        data = data.dict()

        if not "location" in request.data:
            return  Response({"message": "you need to add the location" }, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        serializer = self.serializer_class(data=data)
        
        if user.is_superuser:
            #superuser Will only be able to create managers
            if serializer.is_valid(raise_exception=True): 

                serializer.save()
                
                manager_group = Group.objects.get(name="Manager")                       # Getting the manager Group
                manager = CustomUser.objects.get(username=data['username'])             # Getting the New user created
                manager.user_permissions.add(*manager_group.permissions.all())          # Assigning the group permission to the user
                manager_group.user_set.add(manager)                                     # Adding the user to the group
            else:
                return  Response({"error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "User Created"}, status=status.HTTP_200_OK)
        # MANAGER ONLY 
        elif user.groups.filter(name="Manager").exists():
            # manager will only be able to create employees
            if serializer.is_valid(raise_exception=True): 
                
                if not user.location: #this check if the manager is asigned to a location if not they cant create a employee
                    return  Response({"error": "you can't create a user because you are not assign to a location yet" }, status=status.HTTP_400_BAD_REQUEST)
                
                with transaction.atomic():
                    serializer.save()                                                           # creates a new user
                    
                    employee_group = Group.objects.get(name="Employee")                         # Getting the Employee group 
                    employee = CustomUser.objects.get(username=request.data['username'])        # Getting the new created user
                    employee.location = user.location                                           # Updating the new user location with the manager location
                    employee.save()
                    employee.user_permissions.add(*employee_group.permissions.all())            # Assigning the group permission to the user
                    employee_group.user_set.add(employee)                                       # Assign the employee to the the employee group
            
            else:
                return  Response({"error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_200_OK)


# UPDATE USER INFORMATION
class UpdateUserinformationView( UpdateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):
        try:
            user = request.user
            
            serializer = user_ser.UpdateUsersSerializer(user, data=request.data, partial=True) #This auto cleans the data removes everything that is not in the serializer fields 

            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"message": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

            return  Response({ "message": "updated" }, status=status.HTTP_200_OK)
        
        except:
            return Response({'message': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)


#GET USER PROFILE
class GetUserProfileView( APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # @login_required()
    def get (self, request, format=None):

        if not request.auth is None:
            try:
                user = request.user
                print(user)
                #TODO: CHANGE THE RETURN INFORMATION
                user_profile = user_ser.UserSerializer(user)
            
                return Response({ 'profile': user_profile.data, 'username': str(user.username) })
            except:
                return Response({ 'error': 'Something went wrong when retrieving profile' })
        else:
            return Response(vstatus=status.HTTP_403_FORBIDDEN) 


# This sets the JWT to the black list
class userLogoutView( APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return  Response(status=status.HTTP_403_FORBIDDEN)
        try: 
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return  Response(status=status.HTTP_400_BAD_REQUEST)


#DELETING USER
class DeleteUserView( APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        username = request.user
        try:
            user = CustomUser.objects.get(username = username)
        except:
            return  Response(status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)