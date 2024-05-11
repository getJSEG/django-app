from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from django.contrib.auth.models import Group
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, logout
from django.db import transaction
import json
from rest_framework import status, permissions
from oauth2_provider.settings import oauth2_settings
# from braces.views import CsrfExemptMixin
from oauth2_provider.views.mixins import OAuthLibMixin
from oauth2_provider.views.generic import ProtectedResourceView, ReadWriteScopedResourceView


from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

#this is the new session Authentication
# from rest_framework import permissions


#### MODELS ######
from ..models import CustomUser

##### SERIALIZERZ #####
from ..serializers import user_serializers as user_ser

################################ USER ####################################
########################################################################## 
#CREATING A Customer
# Send to the user to authenticate the new user
class CreateUserView(OAuthLibMixin, APIView):
    permission_classes = (permissions.AllowAny, )
    # serializer_class = user_ser.CreateUsersSerializer

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request, format=None):
        # serializer = self.serializer_class(data=request.data)

        if request.auth is None:
            data = request.data
            data = data.dict()

            serializer = user_ser.CreateUsersSerializer(data=data)
            if serializer.is_valid(raise_exception=True): 
                # try: 
                    with transaction.atomic():
                        serializer.save()
                        user = CustomUser.objects.get(username=request.data['username']) # this catches if theirs a user in DB
                        customer_group = Group.objects.get(name="Customers")
                        user.user_permissions.add(*customer_group.permissions.all())
                        customer_group.user_set.add(user)

                        url, headers, body, token_status = self.create_token_response(request)
                        if token_status != 200:
                            raise Exception(json.loads(body).get("error_description", ""))
                        return Response(json.loads(body), status=token_status)
                # except Exception as e:
                #         return Response(data={"error": e}, status=status.HTTP_400_BAD_REQUEST)
                
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN) 


#This will will only be accesable if the user is a manager or a admin
# @method_decorator(csrf_protect, name='dispatch')
class CreateEmployeeView(ReadWriteScopedResourceView, APIView):
    serializer_class = user_ser.CreateUsersSerializer

    def post(self, request, format=None):

        # if not request.auth is None:
        # return Response(status=status.HTTP_403_FORBIDDEN) 
        

        if not request.user.has_perm('api.add_customuser'):
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
        if not "location" in request.data:
            return  Response({"message": "you need to add the location" }, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        serializer = self.serializer_class(data=request.data)
        
        if user.is_superuser:
            #superuser Will only be able to create managers
            if serializer.is_valid(raise_exception=True): 

                serializer.save()
                
                manager_group = Group.objects.get(name="Manager")                       # Getting the manager Group
                manager = CustomUser.objects.get(username=request.data['username'])     # Getting the New user created
                manager.user_permissions.add(*manager_group.permissions.all())          # Assigning the group permission to the user
                manager_group.user_set.add(manager)                                     # Adding the user to the group
            else:
                return  Response({"error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "User Created"}, status=status.HTTP_200_OK)

        elif user.groups.filter(name="Manager").exists():
            # manager will only be able to create employees
            if serializer.is_valid(raise_exception=True): 
                
                if not user.location: #this check if the manager is asigned to a location if not they cant create a employee
                    return  Response({"error": "you can't create a user because you are not assign to a location yet" }, status=status.HTTP_400_BAD_REQUEST)
                
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
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

        return Response({"message": "User Created"}, status=status.HTTP_200_OK)
        

#cCHECKS USER CREDENTIALS
# @method_decorator(csrf_protect, name='dispatch')
class UserLoginView(APIView):

    permission_classes = [AllowAny]
    serializer_class = user_ser.LoginSerializer
    
    def post(self, request, format=None):
        try:
            if not request.data["username"]or not request.data["password"]:
                return  Response({"error": "These fields may not be blank" }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return  Response({"error": "Something went wrong while loggin in"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get('user')  
            login(request, user)
        else: 
            return Response({"error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
            
        return  Response({"success": "User authenticated"}, status=status.HTTP_200_OK)

# UPDATE USER INFORMATION
class UpdateUserinformationView(ReadWriteScopedResourceView, UpdateAPIView):

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
class GetUserProfileView(ProtectedResourceView, APIView):
    permission_classes = [permissions.IsAuthenticated]
    # TokenHasReadWriteScope( for permission)
    
    def get (self, request, format=None):
        try:
            user = self.request.user
            #TODO: CHANGE THE RETURN INFORMATION
            user_profile = user_ser.UserSerializer(user)
           
            return Response({ 'profile': user_profile.data, 'username': str(user.username) })
        except:
            return Response({ 'error': 'Something went wrong when retrieving profile' })


# LOGOUT USER
class userLogoutView(ReadWriteScopedResourceView, APIView):
    def post(self, request, format=None):
        if not request.user.is_authenticated:
            return  Response({ "message": "Your are not logged in" }, status=status.HTTP_400_BAD_REQUEST)
        try: 
            logout(request)
            return  Response({ "message": "Succefully Logout" }, status=status.HTTP_200_OK)
        except:
            return  Response({ "error": "Something went Wront" }, status=status.HTTP_400_BAD_REQUEST)


#DELETING USER
class DeleteUserView(ReadWriteScopedResourceView, APIView):

    def delete(self, request, format=None):
        username = request.user
        try:
            user = CustomUser.objects.get(username=request.user)
        except:
            return  Response({ "message": "Something went wrong" }, status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()

        return Response({'message': 'No Content'}, status=status.HTTP_204_NO_CONTENT)


