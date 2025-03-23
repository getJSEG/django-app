from rest_framework.response import Response
from rest_framework import status


def not_assiged_location():
    data = { "message": "necesitas ser asignado a una tienda para completar la solicitud." }
    return Response({"data": data}, status=status.HTTP_400_BAD_REQUEST)

def emptyField():
    data = {  "message": "Campo no debe estar vacío" }
    return Response({"data": data}, status=status.HTTP_400_BAD_REQUEST)


def denied_permission():
    data = {  "message": "Permiso Negado" }
    return Response({"data": data}, status=status.HTTP_403_FORBIDDEN)

def expired():
    data = {  "message": "este artículo/promociones ya ha vencido." }
    return Response({"data": data}, status=status.HTTP_400_BAD_REQUEST)

def does_not_exists():
    data = {  "message": "El artículo no existe." }
    return Response({"data": data}, status=status.HTTP_400_BAD_REQUEST)

def already_exists():
    data = {  "message": "Esto ya existe, por favor intente de nuevo." }
    return Response({"data": data}, status=status.HTTP_400_BAD_REQUEST)


def product_already_exist():
    data = {  "message": "Ya existe un producto con el mismo nombre Y marca." }
    return Response({"data": data}, status=status.HTTP_400_BAD_REQUEST)

def varient_already_exists():
    data = {  "message": "Variente con el mismo ID ya existe, porfavor cabie la Talla, color o Medida" }
    return Response({"data": data}, status=status.HTTP_400_BAD_REQUEST)

def invalid_uuid():
    data = {  "message": "ID del articulo Invalido" }
    return Response({"data": data}, status=status.HTTP_400_BAD_REQUEST)