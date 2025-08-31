from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..authenticate import CustomAuthentication

from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _
from django.db import transaction

from rest_framework import status
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core import serializers

#### MODELS ######
from ..models import CustomUser

##### SERIALIZERZ #####
from ..serializers import user_serializers as user_ser
from rest_framework.permissions import AllowAny
import json

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

# from ..repeated_responses.repeated_responses import not_assiged_location, emptyField, denied_permission, product_already_exist, does_not_exists, invalid_uuid

from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
# Utils
from .utils import error_responses


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
        
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# class LoginView(APIView):
    
#     permission_classes = (AllowAny,)

#     def post(self, request, *args, **kwargs):

#         data = request.data
#         response = Response()        

#         username = data.get('username', None)
#         password = data.get('password', None)
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 data = get_tokens_for_user(user)
#                 response.set_cookie(
#                                     'refresh_token',
#                                     # key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
#                                     value = data["refresh"],
#                                     expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
#                                     secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
#                                     httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
#                                     samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
#                                         )
#                 csrf.get_token(request)
#                 # This cone below if for seding the login to an email
#                 # email_template = render_to_string('login_success.html',{"username":user.username})    
#                 # login = EmailMultiAlternatives(
#                 #     "Successfully Login", 
#                 #     "Successfully Login",
#                 #     settings.EMAIL_HOST_USER, 
#                 #     [user.email],
#                 # )
#                 # login.attach_alternative(email_template, 'text/html')
#                 # login.send()
#                 response.data = {'access': data['access']}
#                 # json.dumps(data)
                
#                 return response
#             else:
#                 return Response({"No active" : "This account is not active!!"},status=status.HTTP_404_NOT_FOUND)
#         else:
#             return Response({"Invalid" : "Invalid username or password!!"},status=status.HTTP_404_NOT_FOUND)

def getUserInformation(refresh):

    group_names = []
    try:
        token = RefreshToken(refresh)
        user_id = token['user_id']
        user = CustomUser.objects.get(id = user_id)
        #  this serialize the user groups
        groups = user.groups.all()
        for group in groups:
            group_names.append(group.name)

    except:
        return None
    
    return {"role": group_names, "firstName": user.first_name, "lastname": user.last_name }

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')
"""
Login view 
"""
class LoginView(TokenObtainPairView):
  
  def finalize_response(self, request, response, *args, **kwargs):

    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )

        response.data["user"] = getUserInformation(response.data['refresh'])

        del response.data['refresh'] #removing the  refresh cookie before sending it bacl

    return super().finalize_response(request, response, *args, **kwargs)


""" Refresh token """
class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            # response.set_cookie('roles', getUserInformation(response.data['refresh']), max_age=cookie_max_age, httponly=True )
            # response.data["user"] = getUserInformation(response.data['refresh'])
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer



# TODO: REGISTER
class CreateEmployeeView(RegisterView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = user_ser.CreateUsersSerializer

    def post(self, request, format=None):

        # Checking permission for CusomUser
        if not request.user.has_perm('api.add_customuser'):
            return error_responses.permission_denied()
        
        data = request.data
        data = data.dict()

        if not "location" in request.data:
            return  Response({"message": f"Por favor asigne a {str(data['first_name'].strip().title())} una tienda" }, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        serializer = self.serializer_class(data=data)
        
        if user.is_superuser:
            #superuser Will only be able to create Manager
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
            # Managers will only be able to create Low level Employees
            if serializer.is_valid(raise_exception=True): 
                
                if not user.location: #this check if the manager is asigned to a location if not they cant create a employee
                    return  Response({"message": "No Puedes agregar usuario" }, status=status.HTTP_400_BAD_REQUEST)
                
                with transaction.atomic():
                    serializer.save()                                                           # creates a new user
                    
                    employee_group = Group.objects.get(name="Employee")                         # Getting the Employee group 
                    employee = CustomUser.objects.get(username=request.data['username'])        # Getting the new created user
                    employee.location = user.location                                           # Updating the new user location with the manager location
                    employee.save()
                    employee.user_permissions.add(*employee_group.permissions.all())            # Assigning the group permission to the user
                    employee_group.user_set.add(employee)                                       # Assign the employee to the the employee group
            
            else:
                return  Response({"message": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(status=status.HTTP_200_OK)


"""
    update user information
"""
class UpdateUserinformationView( UpdateAPIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):

        # Checking permission of the user is able to change its profile
        if not request.user.has_perm('api.change_customuser') :
            return error_responses.permission_denied()
        
        try:
            # updating the serializer
            serializer = user_ser.UpdateUsersSerializer(request.user, data=request.data, partial=True) #This auto cleans the data removes everything that is not in the serializer fields 
            #  saving the changes
            if serializer.is_valid():
                serializer.save()
            else:
                return Response({"error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

            return  Response(status=status.HTTP_200_OK)
        
        except:
            return Response({'error': 'Algo salio mal, intente otro rato.' }, status=status.HTTP_400_BAD_REQUEST)


"""
    Retriving the user profile
"""
class GetUserProfileView( APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get (self, request, format=None):

        # Checking permission if it can view custom user
        if not request.user.has_perm('api.view_customuser'):
            return error_responses.permission_denied()

        # checking if its not authenticated/logged in before starting block
        if not request.auth is None:
            try:
                # retriving the user profile
                user_profile = user_ser.UserSerializer(request.user)

                # returning the user profile bac to the front end
                return Response({ 'profile': user_profile.data, 'username': str(request.user.username)})
            except:
                return Response({ 'error': 'usuarion no existe.' })
        else:
            return Response(status=status.HTTP_403_FORBIDDEN) 


"""
    This sets the JWT to the black list
"""
class userLogoutView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # check if the user is authenticated before doing anything
        if not request.user.is_authenticated:
            return  Response(status=status.HTTP_403_FORBIDDEN)
        
        try: 
            # get the refresh token
            # refresh_token = request.data["refresh_token"]
            access_token = request.headers.get("Authorization").split(" ")[1]
            refresh_token = request.COOKIES['refresh_token']
            # validating the refreshtoken
            token = RefreshToken(refresh_token)
            # print("This is the acces token",access_token)
            # print("thi is after the cooke",refresh_token)
            # adding the refresh token to blacklist
            CustomAuthentication().blacklist_token(access_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except:
            return  Response(status=status.HTTP_400_BAD_REQUEST)

class getUserRoles (APIView):
    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # user_id = token['user_id']
        # request.user.groups.all()
        roles = []
        try:
            user = CustomUser.objects.get(id = request.user.id)
        except:
            return  Response(status=status.HTTP_400_BAD_REQUEST)
        #  this serialize the user groups
        groups = user.groups.all()
        for group in groups:
            roles.append(group.name)

        return Response({"roles": roles},status=status.HTTP_200_OK)

"""
Deleteting the user 
"""
class DeleteUserView( APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, format=None):
        # Checking permission if it can delete user
        if not request.user.has_perm('api.delete_customuser'):
            return error_responses.permission_denied()
    
        username = request.user
        try:
            # retriving the user instance
            user = CustomUser.objects.get(username = username)
        except:
            # if it does not exist send back 400 error
            return  Response(status=status.HTTP_400_BAD_REQUEST)
        
        # TODO:Delete the avatar
        # delete the suer
        user.delete()

        # return a 204 status
        return Response(status=status.HTTP_204_NO_CONTENT)