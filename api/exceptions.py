from rest_framework.exceptions import PermissionDenied, APIException
from rest_framework import status

# Custom Exception
class ProductExeption(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST #or whatever you want
    default_code = '4026'
    #  Custom response below
    default_detail = {"code": 4026, "message": "Unable to create product"}




class CustomException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = '4020'
    #  Custom response below
    default_detail = {"code": 4020, "message": "This field cant be empty"}

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code