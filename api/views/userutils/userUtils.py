from rest_framework import status
from rest_framework.response import Response


# this is the user serailzer creation
def userCreationSerializer(data, serializer_class):

    serializer = serializer_class(data=data)

    if serializer.is_valid(raise_exception=True): 
        serializer.save()
    else:
        return  Response({"error": serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "Usuario fue creado exitosamente"}, status=status.HTTP_200_OK)