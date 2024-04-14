from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
import os

#### MODELS ######
from ..models import Products, Varients

##### SERIALIZERZ #####
from ..serializers import product_serializer as productSerializer

#This is inventory Items
class ProductInventoryView(APIView):

    def get(self, request, format=None):
        try:
            if not request.user.has_perm('api.view_products'):
                return Response({'message': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            
            user = request.user

            if not user.location:
                return Response({'message': 'You are not assign to a store'}, status=status.HTTP_400_BAD_REQUEST)
            
            products = Products.objects.filter(location_id = user.location.id)

            if not products.exists():
                return Response({'message': "Not Products in this store yet"}, status=status.HTTP_200_OK)
            
            selializer = productSerializer.GetProductSerializer(products, many=True)

            return Response({'data': selializer.data }, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


# Creating Products
class CreateProductView(CreateAPIView):

    serializer_class = productSerializer.CreateProductSerializer

    def post(self, request, format=None):
        user = request.user

        if not user.has_perm('api.add_products'):
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)
        
        #Chack this validation might need to remove
        if not user.location:
            return Response({"message": "you need a location to be assign to you"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data, context={ 'request': request })
 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'success': serializer.data }, status=status.HTTP_200_OK)


#UPDATING PRODUCTS
class UpdateProductView(APIView):


    def patch(self, request, pk, format=None):
        try: 

            if not request.user.has_perm('api.change_products'):
                return Response({'message': "Permissin denied"}, status=status.HTTP_403_FORBIDDEN)
            
            try: product_instance = Products.objects.get(id=str(pk))
            except: return Response({'message': "product was not found"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = productSerializer.Update(instance=product_instance, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                return Response({'message': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
        
            return Response({'message': "success"}, status=status.HTTP_200_OK)
        
        except:
            return Response({'message': "Something went wrong updating"}, status=status.HTTP_400_BAD_REQUEST)

#DELETING PRODUCTS
class DeleteProductView(APIView):
    
    def delete(self, request, product_id, *args, **kwargs):  
        try:
            if not request.user.has_perm('api.delete_products'):
                return Response({'message': "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

            try: 
                product = Products.objects.get(id=product_id)
            except: 
                return Response({'message': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
            
            varient_instance = Varients.objects.filter(product_id=product_id)

            if not varient_instance.exists():
                product.delete()
                return Response({'message': "Not Content"}, status=status.HTTP_204_NO_CONTENT)
            else:
                for varient in varient_instance:                        # Looping through the varients
                    if not varient.album == 'None':                     # Check if varients has an album 
                        images = varient.album.images.all()             # Getting all of the images
                        varient_colors = varient.album.varient_colors.all()     # Getting all of the varients
                        for color in varient_colors :                   # Looping thorug the Color varients
                            os.remove(color.color.path)                 # Removing/deleting the COLOR images from computer/OS 
                            color.delete()                              # Deleting the actual Model
                        for image in images :       
                            os.remove(image.image.path)                 # Removing/deleting the images from computer/OS 
                            image.delete()                              # Deleting the image model
                        varient.album.delete()                          # Deleting the album model
                    varient.delete()                                    # Deleting the Varient model
                product.delete()                                        # Delete the product model
            
            return Response({'message': "Not Content"}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)






