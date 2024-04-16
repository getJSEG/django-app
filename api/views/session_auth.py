from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.hashers import make_password, check_password

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator

#this is the new session Authentication
from rest_framework import permissions
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect


#SETS CSRF TOKEN TO USER WHEN FIRST CALLED
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        print("this is called")
        return Response({ 'isAutheticated': 'CSRF cookie set' })
    
#CHECK AUTHENTICATION
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated
            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })

