from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.models import Group

from django.utils.translation import gettext_lazy as _
from django.db import transaction

from rest_framework import status
from dj_rest_auth.registration.views import RegisterView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

#### MODELS ######
from ..models import CustomUser

##### SERIALIZERZ #####
from ..serializers import user_serializers as user_ser
from rest_framework.permissions import AllowAny
import json

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

from ..repeated_responses.repeated_responses import not_assiged_location, emptyField, denied_permission, product_already_exist, does_not_exists, invalid_uuid

from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf

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
#                 print(data)
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


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        print('refresh is sent back')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

class LoginView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
        del response.data['refresh']
    return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer



# TODO: REGISTER
class CreateEmployeeView(RegisterView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = user_ser.CreateUsersSerializer

    def post(self, request, format=None):

        if not request.user.has_perm('api.add_customuser'):
            return denied_permission()
        
        data = request.data
        data = data.dict()

        if not "location" in request.data:
            return  Response({"message": f"Por favor asigne a {str(data['first_name'].strip().title())} una tienda" }, status=status.HTTP_400_BAD_REQUEST)

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
                #TODO: CHANGE THE RETURN INFORMATION
                user_profile = user_ser.UserSerializer(user);
            
                return Response({ 'profile': user_profile.data, 'username': str(user.username)})
            except:
                return Response({ 'error': 'Something went wrong when retrieving profile' })
        else:
            return Response(status=status.HTTP_403_FORBIDDEN) 


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
            return Response(status=status.HTTP_200_OK)
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