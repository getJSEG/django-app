from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..authenticate import CustomAuthentication
# from django.utils.translation import gettext_lazy as _
from rest_framework import status
from dj_rest_auth.registration.views import RegisterView
#### MODELS ######
from ..models import CustomUser

##### SERIALIZERZ #####
from ..serializers import user_serializers as user_ser

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.user.user_serializer import userSerializer

# Utils
from .utils import error_responses
from .userutils.userUtils import userCreationSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

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


"""
    Creating emploee base on the Group
"""
class CreateEmployeeView(RegisterView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = userSerializer

    def post(self, request, format=None):

        # Checking permission for CusomUser
        if not request.user.has_perm('api.add_customuser'):
            return error_responses.permission_denied()
        
        data = request.data

        if not "location" in request.data:
            return  Response({"details": "El campo de Local es obligatorio." }, status=status.HTTP_400_BAD_REQUEST)
        if not data["location"]:
            return  Response({"details": "El campo de Local es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        # This superuser can create Owner
        if user.is_superuser:
            data["position"] = "Owner"
            return userCreationSerializer(data, self.serializer_class)
        #Owners can only create managers and employees
        elif user.groups.filter(name="Owner").exists():
            if not "position" in data:
                return  Response({"details": "El campo de posición es obligatorio." }, status=status.HTTP_400_BAD_REQUEST)
            if not data["position"]:
                return  Response({"details": "El campo de posición es obligatorio." }, status=status.HTTP_400_BAD_REQUEST)
            
            return userCreationSerializer(data, self.serializer_class)
        # manager can only create employee
        elif user.groups.filter(name="Manager").exists():
            data["position"] = "Employee"
            return userCreationSerializer(data, self.serializer_class)
        
"""
    update user information
"""
class UpdateUserinformationView(UpdateAPIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):

        # Checking permission of the user is able to change its profile
        if not request.user.has_perm('api.change_customuser') :
            return error_responses.permission_denied()
        
        try:
            # updating the serializer
            # get user here 
            user_instance = CustomUser.objects.get(username = request.user.username)
            serializer = userSerializer(user_instance, data=request.data, partial=True)
            # serializer = user_ser.UpdateUsersSerializer(request.user, data=request.data, partial=True) #This auto cleans the data removes everything that is not in the serializer fields 
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
class GetUserProfileView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get (self, request, format=None):
        # Checking permission if it can view custom user
        if not request.user.has_perm('api.view_customuser'):
            return error_responses.permission_denied()
        # checking if its not authenticated/logged in before starting block
        if not request.auth is None:
            try:
                user_serializer = CustomUser.objects.get(username = request.user)
                # retriving the user profile
                # user_serializer = CustomUser.objects.get(username = request.user)
                # user_profile = userSerializer(request.user)
                user_profile = userSerializer(user_serializer)
                # returning the user profile bac to the front end
                return Response({ 'profile': user_profile.data})
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
            CustomAuthentication().blacklist_token(access_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except:
            return  Response(status=status.HTTP_400_BAD_REQUEST)


# class getAllRolesView (APIView):
#     authentication_classes = [CustomAuthentication, JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, format=None):
        
#         return Response({"roles": roles},status=status.HTTP_200_OK)


class getUserRoles (APIView):
    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        roles = []
        try:
            user_intance = CustomUser.objects.get(id = request.user.id)
        except:
            return  Response(status=status.HTTP_400_BAD_REQUEST)
        #  this serialize the user groups
        groups = user_intance.groups.all()
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