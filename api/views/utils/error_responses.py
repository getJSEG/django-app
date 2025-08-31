
from rest_framework.response import Response
from rest_framework import status

# response for pemission denied
def permission_denied():
    return Response({ "error":  "Permiso Negado" }, status=status.HTTP_403_FORBIDDEN)

def location_not_assigned():
    return Response({ "error":  "usuaria no a sido asignado" }, status=status.HTTP_400_BAD_REQUEST)


def something_went_wrong():
    return Response({ "error":  "Algo salio mal" }, status=status.HTTP_400_BAD_REQUEST)