from django.db import models
from rest_framework import status
from rest_framework.response import Response
from ...models import ReceiptLine, Varient, Order


def get_and_update_variante(instance_sku, instance_quantity):
    # retriving the variante instance
    try:
        variante_instance = Varient.objects.get(sku=instance_sku)
        # getting the unite and adding back the units that is deleted
        variante_instance.units = variante_instance.units + instance_quantity
        # saving the variant instance
        variante_instance.save()
    except:
        pass
    return

# loops trough all of the items re-calculates the subtotal and updates the total amount after deleting one item
def update_shipping_order_total(model_instance, order_id) :
    total = 0
    try:
        order_instance = Order.objects.get(id=order_id)
        all_line_items = ReceiptLine.objects.filter(order=order_id)

        for item in all_line_items:
            total = total + item.subtotal

        order_instance.totalAmount = total
        order_instance.save()
    except:
        pass

# This function deletes if the package is processing only
# 1. deletes the whole model instance or
# 2. deletes only the order line item if fields are provided
def delete_package(model_instance, request):
    instance_status = ""
    

    if(hasattr(model_instance,"status")):
        print("has status", model_instance.status)
        instance_status = model_instance.status
    else:
        response =  Response({"detail": "Error: 122131"}, status=status.HTTP_204_NO_CONTENT) 
        return response

    if instance_status == "SHIPPED" : 
        response =  Response({"detail": "No se puede editar o modificar por que el paquete ya fue enviado"}, status=status.HTTP_400_BAD_REQUEST) 
        return response
    elif instance_status == "DELIVERED" :
        response =  Response({"detail": "No se puede editar o modificar por que el paquete fue entregado"}, status=status.HTTP_400_BAD_REQUEST) 
        return response
    
    if(instance_status != "PROCESSING"):
        response =  Response({"detail": "no se puede editar o modificar por el estado"}, status=status.HTTP_400_BAD_REQUEST) 
        return response

    # getting the parameters that are necesary for deletion
    package_id = request.GET.get('package', None)
    order_id = request.GET.get('order', None)
    order_line_id = request.GET.get("item", None)


    if (order_line_id != '' and order_line_id != '') and (order_id is not None and order_line_id is not None):
        # Delete the receipt line only 
        receipt_line_instance_arr = receipt_line_instance = ReceiptLine.objects.filter(id=order_line_id, order=order_id)
        if not receipt_line_instance_arr.exists():
            response =  Response({"detail": "Producto No Existe."}, status=status.HTTP_204_NO_CONTENT) 
            return response
        # this get the firt line item of the array
        receipt_line_instance = receipt_line_instance_arr[0]
        
        # this prevents from the user deleting the product if theirs is only 1 in the package
        if len(model_instance.shippingOrder.OrderLine.all()) == 1 :
            response = Response({"detail": "No  se puede borrar, Al menos 1 producto debe estar en el paquete"}, status=status.HTTP_400_BAD_REQUEST) 
            return response
        else:
            get_and_update_variante(receipt_line_instance.sku, receipt_line_instance.quantity)
            receipt_line_instance.delete()
            # this updates the total amount in order price
            update_shipping_order_total(model_instance, order_id)

            response =  Response({"detail": "product fue borado"}, status=status.HTTP_200_OK) 
            return response

        # finalize deletetion of the Order line item
        return
    if (package_id is not None and package_id != '') and (order_line_id == '' and order_line_id == ''):
        # loop throu all of the line items and update back the variant units
        all_line_items  = ReceiptLine.objects.filter(order=model_instance.shippingOrder.id)
        if all_line_items.exists():
            for item in all_line_items:
                get_and_update_variante(item.sku, item.quantity)
                item.delete()
        
        model_instance.shippingOrder.delete()
        model_instance.delete()
        response =  Response({"detail": "product fue borado"}, status=status.HTTP_200_OK) 
        return response

    return None 

