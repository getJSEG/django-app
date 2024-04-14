from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
import re
import os

#this is the new session Authentication
from rest_framework import permissions
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

#### MODELS ######
from ..models import CustomUser                                   #user
from ..models import Products                                     #product
from ..models import Varients, VarientImages, VarientColors, ImageAlbum       #varients
##### SERIALIZERZ #####
from ..serializers import varients_serializer

from ..helper import generate_sku

#CREATING VARIENT
class CreateVarientView(APIView):
    queryset = Varients.objects.all()
    serializer_class = varients_serializer.CreateVarientSerializer

    def post(self, request, pk):
        try:
            if not request.user.has_perm('api.add_varients'):
                return Response({'error': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)

            try:
                product = Products.objects.get(id=pk)  #getting the product by id
            except product.DoesNotExist:
                return Response({"error": 'Product not found' }, status=status.HTTP_400_BAD_REQUEST)
        
            album = ImageAlbum.objects.create()    

            varient_img_raw_data = {}
            varient_color_raw_data = {}     

            try: 
                sku = generate_sku(request.data, request.data["brand"], product.id)
            except:
                return Response({'message': 'Something went wrong when creating the SKU'}, status=status.HTTP_400_BAD_REQUEST)

            # create varient image
            try:
                images = request.data.pop('images')
                for image in images:
                    varient_img_raw_data['image'] = image
                    varient_img_raw_data['album'] = album.id
                    varient_image =  varients_serializer.CreateVarientImageSerializer(data=varient_img_raw_data)

                    if varient_image.is_valid(raise_exception=True):
                        varient_image.save()
                    else:
                        return Response({"error": varient_image.errors}, status=status.HTTP_400_BAD_REQUEST)
            except:
                album.delete()                                                                                                  # Delete Album if somthing went wront creating images
                return Response({'error': 'Something went wrong saving the images' }, status=status.HTTP_400_BAD_REQUEST)

            #creating varient color
            try:
                varient_color_raw_data['color'] = request.data.pop('varient_color_image')[0]
                varient_color_raw_data['description'] = str(request.data.pop('description')[0])
                varient_color_raw_data['album'] = album.id
                
                color_image = varients_serializer.CreateVarientColorsSerializer(data=varient_color_raw_data)

                if color_image.is_valid(raise_exception=True):
                    color_image.save()
                else:
                    return Response({"error": color_image.errors}, status=status.HTTP_400_BAD_REQUEST)
            except:
                # album.delete()
                # # varient_image.delete()
                # color_image.delete()
                return Response({'error': 'Something went wrong saving color varients' }, status=status.HTTP_400_BAD_REQUEST)
            
            # Creating  varients
            request.data['album'] = album.id
            request.data['sku'] = sku
            request.data['product_id'] = product.id
            request.data['location_id'] = request.user.location.id

            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "varient created successfully"}, status=status.HTTP_200_OK)
        
        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)




#TODO: SEARCH ITEM
#TODO: CHECK IF ITEM HAS SOLD OUT
#TODO: CREATE AND REMINDER TO IF ITEMS ARE RUNNING LOW
class GetVarientView(APIView):

    def get(self, request, product_id, *args, **kwargs):
        user = request.user

        if not user.has_perm('api.view_varients'):
            return Response({"message": 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)   


        queryset = Varients.objects.filter(product_id=product_id, location_id=user.location)

        if not queryset.exists():
            return Response({"message": 'Product Doesnt have varient'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = varients_serializer.GetVarientSerializers(queryset, many=True)
        return Response({'data': serializer.data }, status=status.HTTP_200_OK) # if nothing was found



#updating view
class UpdateVarientView(APIView):

    def patch(self, request, pk, *args, **kwargs):
        # Checking permissions
        if not request.user.has_perm('api.change_varients'):
            return Response({'message': 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN)
        
        varient_id = str(pk).strip()
        data = request.data
        varient_instance = Varients.objects.filter(id=varient_id)
        varient_image_raw_data = {}
        varient_color_raw_data = {}                                                 

        if "brand" in data: brand = data["brand"]
        else: brand = varient_instance[0].brand

        # Updating SKU
        try: sku = generate_sku(request.data, brand, varient_instance[0].product_id.id )
        except: return Response({'message': 'Something went wrong creating SKU'}, status=status.HTTP_400_BAD_REQUEST)

        #updating varient colors and replace the image with new image
        if 'description' in data:
            varient_color_raw_data['description'] = data.pop('description')[0]
        if 'color_varient' in data:
            varient_color_raw_data['color_varient'] = data.pop('color_varient')[0]

        varient_color_intance = VarientColors.objects.filter(album=varient_instance[0].album.id)

        if varient_color_intance.exists():
            varient_color_serlializer = varients_serializer.UpdateVarientColorsSerializer(instance=varient_color_intance[0], data = varient_color_raw_data, partial=True)

            if varient_color_serlializer.is_valid():
                varient_color_serlializer.save()
            else: 
                return Response({'error': varient_color_serlializer.errors }, status=status.HTTP_400_BAD_REQUEST)


        #updating Varient Colors

        varient_images_instance = VarientImages.objects.filter(album=varient_instance[0].album.id)      # getting images
    
        if 'images' in data:
            # If the image has more that 6 images just replace them if not create new up to 6
            
            images = data.pop('images')
            if len(varient_images_instance) >= 6:
                initial = 0
                while initial >= 6:
                    if initial >= len(varient_images_instance):
                        varient_image_raw_data['image'] = images[initial]
                        updating_partia_varient_images= varients_serializer.UpdateVarientImageSerializer(intance=varient_images_instance[0], data=varient_image_raw_data, partial=True)

                        if updating_partia_varient_images.is_valid():
                            updating_partia_varient_images.save()
                        else: 
                            return Response({'error': updating_partia_varient_images.errors }, status=status.HTTP_400_BAD_REQUEST)
                        
                    elif initial < len(varient_images_instance):
                        #creating new images until you hit 6
                        varient_image_raw_data['image'] = images[initial]
                        varient_image_raw_data['album'] = varient_instance[0].album.id
                        varient_image =  varients_serializer.CreateVarientImageSerializer(data=varient_image_raw_data)

                        if varient_image.is_valid(raise_exception=True):
                            varient_image.save()
                        else:
                            return Response({"error": varient_image.errors}, status=status.HTTP_400_BAD_REQUEST)
                        pass
                    initial += 1
                
            else:   
                # updating all of the images
                for image in images:
                    
                    varient_image_raw_data['image'] = image
                    updating_varient_images = varients_serializer.UpdateVarientImageSerializer(instance=varient_images_instance[0], data=varient_image_raw_data, partial=True)

                    if updating_varient_images.is_valid():
                        updating_varient_images.save()
                    else: 
                        return Response({'error': updating_varient_images.errors }, status=status.HTTP_400_BAD_REQUEST)

        # Update varient
        varient_serializer= varients_serializer.UpdateVarientImageSerializer(instance=varient_instance[0], data = data, partial=True)

        if varient_serializer.is_valid():
            varient_serializer.save()
        else: 
            return Response({'error': varient_serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'success' }, status=status.HTTP_200_OK)


class DeleteMultipleVarientView(RetrieveAPIView):

    def post(self, request, *args, **kwargs):
        try:
            if not request.user.has_perm('api.delete_varients'):
                return Response({"message": 'Permission Denied'}, status=status.HTTP_403_FORBIDDEN) 
            
            delete =  request.data['delete']
            for value in delete:
                clean_value = re.sub(r'[^a-zA-Z0-9-]',"", value)                       #This does a basic cleaning of the string before searching the DB
        
                try: 
                    varient_instance = Varients.objects.get(id=clean_value, product_id=kwargs['pk'])
                
                    if not varient_instance.album == 'None':                            # when the album is None or empty
                        images = varient_instance.album.images.all()                    # Getting all of the Varient Images
                        varient_colors  = varient_instance.album.varient_colors.all()   # Getting all of the Varient Color Images

                        for color in varient_colors:                                    # Looping throught the Colors Images
                            os.remove(color.color.path)                                 # Deleting the actual file from the OS
                            color.delete()                                              # Deleting the Varient Color Table 

                        for image in images:                                            # Looping throught the Colors Images
                            os.remove(image.image.path)                                 # Deleting the actual file from the OS
                            image.delete()                                              # Deleting the Varient Color Table 

                        varient_instance.album.delete()                                 # Deleting the album Table

                    varient_instance.delete()                                           # Finaly Deleting the Varient

                except Varients.DoesNotExist:
                    return Response({"message": 'Varient Not Found'}, status=status.HTTP_400_BAD_REQUEST) 
                
            return Response({"message": 'Not content'}, status=status.HTTP_204_NO_CONTENT) 
        except:
            return Response({"message": 'Something went wrong deleting'}, status=status.HTTP_400_BAD_REQUEST) 








#TODO: ADD EXTRA PROTECTION TO THIS ROUTE BEAUSE IT WILL BE ACCESIBLE TO ANY ONE
#TODO: CREATE A SEARCH TAGS  OR NAMES
# class GetProductsView(APIView):

#     def get(self, request, *args, **kwargs):
#         user = request.user

#         if not user.has_perm('api.view_products'):
#             return Response({'Error': "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

#         products = Products.objects.all()

#         selializer = p.GetProductSerializer(products, many=True)

#         return Response({'data': selializer.data }, status=status.HTTP_200_OK)
