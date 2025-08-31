from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, F, Sum, Count, Avg
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ...authenticate import CustomAuthentication

# Import serilizer
from ...serializers import product_serializer
from ...repeated_responses.repeated_responses import denied_permission

from ...models import Categories

class CategoryView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    categorySerializer  = product_serializer.CategorySerializer

    def post(self, request, format=None):

        # Permissions
        if not request.user.has_perm('api.add_tags'):
            return denied_permission()
        
        data = request.data.copy()
        # TODO: Double check if the user has a location else Trow an eerror BOTH POST AND GET
        data.update({ "location":  request.user.location.id })

        serializer = self.categorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'data':  serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

        return Response({ "data": "creado"}, status=status.HTTP_200_OK)


    def get(self, request, format=None):
        # Permissions
        if not request.user.has_perm('api.view_tags'):
            return denied_permission()

        category = Categories.objects.filter(location = request.user.location.id)

        serializer = self.categorySerializer(category, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Delete

# Update


# Get