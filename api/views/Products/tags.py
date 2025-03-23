from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q, F, Sum, Count, Avg
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import uuid
import requests
import json


# Import serilizer
from ...serializers import product_serializer
from ...repeated_responses.repeated_responses import denied_permission

from ...models import Tags

# Create
class tagsView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    tagSerializer  = product_serializer.TagSerializer

    def post(self, request, format=None):

        # Permissions
        if not request.user.has_perm('api.add_tags'):
            return denied_permission()
        
        data = request.data.copy()
        # TODO: Double check if the user has a location else Trow an eerror BOTH POST AND GET
        data.update({ "location":  request.user.location.id })

        serializer = self.tagSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'data':  serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

        return Response({ "data": "creado"}, status=status.HTTP_200_OK)


    def get(self, request, format=None):
        # Permissions
        if not request.user.has_perm('api.view_tags'):
            return denied_permission()

        tags = Tags.objects.filter(location = request.user.location.id)

        serializer = self.tagSerializer(tags, many=True)

        return Response({ "data": serializer.data}, status=status.HTTP_200_OK)
# Get

# Delete


# Update