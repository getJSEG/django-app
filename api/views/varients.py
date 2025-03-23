from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from django.db import transaction
from django.db.models import Q

import uuid
import requests

#this is the new session Authentication
from rest_framework import permissions
from urllib.parse import urlencode

##### SERIALIZERZ #####
from ..serializers import product_serializer
from ..models import Varient, Product

from ..helper import generate_sku, generate_presign_url
from django.conf import settings

# Functions
from ..repeated_responses.repeated_responses import not_assiged_location, denied_permission, does_not_exists, invalid_uuid, emptyField, varient_already_exists
from ..helper_classes.varients import required_info_Validation, cleanString, info_require_for_update

# This Create Varient
# TODO: If theirs not varientImage dont send to get a presign url
# TODO: Product info get removed when updating
class VarientView(APIView):

    # Require Authentication
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    varientSerializer = product_serializer.VariantOnlySerializer

    def post(self, request, format=None):

        # Checking Permission
        if not request.user.has_perm('api.add_varient'):
            return denied_permission()

        data = request.data.copy()
        product_id = data["product"]
        try:
            uuid_obj = uuid.UUID(product_id, version=4) #Value Error
        except:
            return invalid_uuid()
        
        product = Product.objects.filter(Q(id=product_id))

        if not product.exists():
            return does_not_exists()

        # Validation required Infor
        is_info_valid, info_err_message = required_info_Validation(data)
        if not is_info_valid:
            return Response({"data": { "message": info_err_message}}, status=status.HTTP_400_BAD_REQUEST)

        sku = generate_sku(product[0].name, product[0].brand, data['size'], data['color'], product[0].id)
        data["sku"] = sku
        varientFound = Varient.objects.filter(Q(sku__icontains=sku))

        if varientFound.exists():
            return varient_already_exists()
        
        if 'varientImage' in data:
            # A list of presigned url to sen to the front end
            presignedUrlList = []
            # Sending request to get presined URL
            presignedUrl = generate_presign_url()
            presignedUrlList.append(presignedUrl["uploadURL"])

            url = settings.CLOUDFLARE_IMAGES_DOMAIN
            account_hash = settings.CLOUDFLARE_ACCOUNT_HASH

            data["varientImage"].update({
                "cf_id": presignedUrl["id"],
                # "link":f"https://{url}/{account_hash}/{presignedUrl["id"]}/public"
            })

        serializer = self.varientSerializer(data=data)

        with transaction.atomic():
            if  serializer.is_valid(raise_exception=True):
                    serializer.save()
            else:
                raise Exception(serializer.errors)
        
        return Response({"data": {"message": "Variente Creado Exitosamente", "upload": presignedUrlList}}, status=status.HTTP_201_CREATED)



# TODO: Make Sure the SKU is regenerated if the item color and size is change else dont change
#updating view
class UpdateVarientView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    varientSerializer = product_serializer.VariantOnlySerializer

    def patch(self, request, *args, **kwargs):
        user = request.user
        # Checking permissions
        if not user.has_perm('api.change_varient'):
            return denied_permission()
        
        variantId = request.GET.get('variant').strip()
        data = request.data.copy()
        
        if_info_valid, update_infor_err_msg = info_require_for_update(variantId, data)
        if not if_info_valid:
            return Response({"data": { "message": update_infor_err_msg}}, status=status.HTTP_400_BAD_REQUEST)
        
        # This Removes the Variant Image we are not updating image in this view
        if "varientImage" in data:
            data.pop('varientImage')

        try:
            product_uuid = uuid.UUID(variantId, version=4)
        except:
            return invalid_uuid()
        
        try: variant_instance = Varient.objects.get(Q(id=variantId))
        except: return does_not_exists()

        serializer = self.varientSerializer(instance=variant_instance, data=data, partial=True)
        try:
            with transaction.atomic():
                if  serializer.is_valid(raise_exception=True):
                        serializer.save()
                else:
                    raise Exception(serializer.errors)
        except (Exception, ValueError) as e:
            return Response({"data": {"message": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': { "message" : "Actualizado Exitosamente"} }, status=status.HTTP_200_OK)


#This View Delete Varients
class DeleteVarientView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk ,*args, **kwargs):
        # Check Premission for the user
        user = request.user
        if not user.has_perm('api.delete_varient'):
            return denied_permission()

        # variantId = request.GET.get('variant') 
        variantId = pk

        if not variantId:
            return Response({"data": {"message":'Informacion Requerida'}}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            variant = Varient.objects.get(id=variantId)

            if (len(variant.product.variants.all()) == 1):
                return Response({"data": {"message": 'No Puedes Borrar Variente porque solo hay 1'}}, status=status.HTTP_400_BAD_REQUEST)
            # send the link to cloudflare
            if (variant.varientImage):
                if(variant.varientImage.cf_id):
                    url = f"https://api.cloudflare.com/client/v4/accounts/{settings.CLOUDFLARE_ACCOUNT_ID}/images/v1/{variant.varientImage.cf_id}"
                    headers = {"Authorization": f"Bearer {settings.CLOUDFLARE_API_KEY}"}
                    response = requests.delete(url, headers=headers)

                    response.raise_for_status()
                    if response.status_code >= 200 and response.status_code <= 299:
                        with transaction.atomic():
                            variant.varientImage.delete()
                    else:
                        return Response({"data": { "message": 'No se puede borrar variente en este momento, Intente despues.' }}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            with transaction.atomic():
                variant.delete()
        except Exception as e:
            return Response({"data": { "message": str(e) } } , status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)