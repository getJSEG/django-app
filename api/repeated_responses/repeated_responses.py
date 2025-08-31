from rest_framework.response import Response
from rest_framework import status


def not_assiged_location():
    data = { "error": "necesitas ser asignado a una tienda para completar la solicitud." }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

def emptyField():
    data = {  "error": "Campo no debe estar vacío" }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


def denied_permission():
    data = {  "error": "Permiso Negado" }
    return Response({"data": data}, status=status.HTTP_403_FORBIDDEN)

def expired():
    data = {  "error": "este artículo/promociones ya ha vencido." }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

def does_not_exists():
    data = {  "error": "El artículo no existe." }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

def already_exists():
    data = {  "error": "Esto ya existe, por favor intente de nuevo." }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


def product_already_exist():
    # data = {  "message": "Ya existe un producto con el mismo nombre Y marca." }
    return Response({"error": "Ya existe un producto con el mismo nombre Y marca."}, status=status.HTTP_400_BAD_REQUEST)

def varient_already_exists():
    data = {  "error": "Variente con el mismo ID ya existe, porfavor cabie la Talla, color o Medida" }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)

def invalid_uuid():
    data = {  "error": "ID del articulo Invalido" }
    return Response(data, status=status.HTTP_400_BAD_REQUEST)