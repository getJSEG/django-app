from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from django.db.models import Q
from ..helper import store_number_generator

# Authentication and permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..authenticate import CustomAuthentication

#### MODELS ######
from ..models import CustomUser, Location

# Serializer
from ..serializers import location_serializer 


# this returns all of the information from ALLL locations this will not be 
class LocationView(APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        if not request.user.has_perm('api.view_location'):
            return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = CustomUser.objects.get(username=request.user)
        except:
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

        # print(user)
        # if(not user.is_superuser or not user.is_staff):
        #     return Response({"message": "You dont have permission"}, status=status.HTTP_403_FORBIDDEN)

        # results = Location.objects.filter(city__icontains=request.GET.get('city') ) 
        results = Location.objects.filter(id=user.location.id )
        # If it donse exist the return empmty object
        if not results.exists():
            return Response({"data": {}}, status=status.HTTP_400_BAD_REQUEST)
        # results = Locations.objects.filter(city__icontains=user.location.id)
        result = results[0]
        # queryset = Locations.objects.all()
        location = location_serializer.LocationSerializer(result)

        return Response(location.data, status=status.HTTP_200_OK)


# TODO: check if the query is one and set it to empty string this way the front end doesen require it to accep the research
# aslo wrsp this is a try except method
class SearchLocation(CreateAPIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, forman=None):
        city = request.GET.get('city')
        country = request.GET.get('country')
        storeNumber = request.GET.get('storeNumber')

        results = Location.objects.filter(Q(city__icontains= city) | Q(country__icontains=country) | Q(storeNumber__icontains=storeNumber))

        locations = location_serializer.LocationSerializer(results, many=True)

        return Response({"data": locations.data }, status=status.HTTP_200_OK)



# CREATE LOCATION
# TODO: Use atomic with this 
class CreateLocationView( CreateAPIView):
    
    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = location_serializer.CreateLocationSerializer

    def post(self, request, format=None):
        try:

            if not request.user.is_superuser:                                               #Permission only for admin
                return Response({"message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
            
            data = request.data.copy()
            
            country = str(data["country"])
            location_type = str(data["locationType"])

            store_number = store_number_generator(location_type, country)
            location = Location.objects.filter(storeNumber = store_number)

            if not location.exists():                                                       #if the location does not exist on first search same the store_number
                data["storeNumber"] = store_number
            else:
                while location.exists():                                                    #else loop until you get a new store number that does not exist
                    store_number = store_number_generator(location_type, country)
                    location = Location.objects.filter(storeNumber = store_number)
                data["storeNumber"] = store_number

            serializer = self.serializer_class(data=data)   

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"data": serializer.data }, status=status.HTTP_200_OK)
        
        except:
            return Response({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

#updated 
class UpdateLocationView( UpdateAPIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):
        try:
            # if its a super user it can update any location info
            if request.user.is_superuser:                                                                                                   #Permission only for admin
                data = request.data.copy()

                if not 'location' in data:
                    return Response({'message': 'Provide a Location'}, status=status.HTTP_400_BAD_REQUEST)
                
                location = data.pop('location')

                try:
                    location_instance = Location.objects.get(id=location[0])
                except:
                    return Response({'message': 'Location does not exist'}, status=status.HTTP_400_BAD_REQUEST) 

                serializer = location_serializer.UpdateLocationSerializer(location_instance, data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({"message": serializer.errors }, status=status.HTTP_400_BAD_REQUEST) 
                
                return Response({'message': 'Success'}, status=status.HTTP_200_OK)
            #If not a super user Update to assigned locations only
            elif request.user.has_perm('api.view_locations'):                                                                             #check permission for user 
            
                user_location = request.user.location                                                                                       #This get the location assign to the manager or owner

                serializer = location_serializer.UpdateLocationSerializer(user_location, data=request.data, partial=True)                    #This auto cleans the data removes everything that is not in the serializer fields 

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                else:
                    return Response({"message": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#ONLY ADMIN CAN DELETE ANY LOCATION
class DeleteLocationView( APIView):

    authentication_classes = [CustomAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, form=None):
        try:
            if not request.user.is_superuser:
                return Response({'message': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                location = Location.objects.get(id=pk)
            except:
                return Response({'message': 'This Location Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            location.delete()

            return Response({'message': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)