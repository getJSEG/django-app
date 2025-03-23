from decimal import Decimal


from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from ..models import Varient, Location


def float_to_decimal(float):
    return Decimal(format(Decimal(float), ".2f"))

def checkout_data_required(data):
    listRequired = ['paymentInfo', 'items', 'subtotal', "includeTaxes", 'includeDiscount', 'discount', 'taxes', 'grandTotal']
        
    for list_item in listRequired:
        if not list_item in data:
            return False, f"{list_item} requerido"
        else:
            if data[list_item] == "":
                return False, f"{list_item} no deve estar blanco"
    return True, ""

# Verifying the information
def payment_data_required(paymentInfo, data):
    # CCInfoRequired = ['ccnumber', 'cvv', 'month', 'year']
    ccInforRequired = ['transaction_id', 'cc_last_digits']
    customerinfoRequired = ['dui', 'phone']
    grandTotal = float_to_decimal(data['grandTotal'])

    if not 'payment_type' in paymentInfo:
        return False, "Tipo de pago requerido"   
    
    paymentType = paymentInfo['payment_type'].strip().lower()
    
    if paymentType == 'credit_card' or paymentType == 'debit_card':
        if not len(str(paymentInfo['cc_last_digits'])) == 4:
            return False, "Ultimos 4 digitos de la targeta requerido"
    
        if grandTotal >= 100:
            if not 'customerInfo' in data:
                return False, "Información del cliente requerida para pagos realizados con tarjeta superior a $100"
            
            for customerInfo in customerinfoRequired:
                if not customerInfo in data['customerInfo']:
                    return False, f"{customerInfo} Informacion Requerida"
   
        for ccInfo in ccInforRequired:
            if not ccInfo in paymentInfo:
                return False, f"{ccInfo}: Informacion Requerida"
 
    elif paymentType == 'cash':
        if not 'TotalReceived' in paymentInfo:
            return False, "Total recivido requerido, porfavor entre en total que recivio en efectivo."
    
    elif paymentType == 'bank_transfer':
        if not 'bank_transfer_code' in paymentInfo:
            return False, "Codigo de tranferencion requerido"
    
    return True, ""

# Cross Checking each product for price, units, and existance to the database 
def checkInventory(items):
    if len(items) <= 0:
        return False, "por favor agregue un mínimo de 1 producto"
    
    for item in items:
        varient = Varient.objects.filter(Q(sku = item['sku']))
        if item['units'] <= 0:
            return False, "las unidades deben ser mayores que 0"
        if not varient.exists():
            return False, f"Producto {item['name']} no existe, porfavor elimine el articulo"
        if varient[0].units < item['units']:
            return False, f"No hay suficientes {item['name']}, solo hay {varient[0].units} en el inventario."
        if not varient[0].price == float_to_decimal(item['price']):
            return False, "El precio no coinside con el precio en el invetario."
        
    return True, ""

# cross checking data base to see if the grand total matches the incoming data
def calculate_order_amount(items, data, location):
    grandTotal = 0
    is_tax_included =  data['includeTaxes']
    is_discount_included = data['includeDiscount'] 
    discount = data['discount']
    print(data)
    # call database and check for the price of the back end 
    for item in items:
        productInstance = Varient.objects.get(sku = item["sku"] )
        itemPrice = int(item['units']) * productInstance.price
        grandTotal = grandTotal + itemPrice
    
    # Check Subtotal before moving to the other grand total
    if not float_to_decimal(data['subtotal']) == grandTotal:
        return False, "Subtotal no coincide con el subtotal proporcionada"
    
    # Calcualte the taxes of the store
    if is_discount_included: 
        disc = (float_to_decimal(discount)/100) * grandTotal
        grandTotal = grandTotal - float_to_decimal(disc)

    # check fron-end and back-end if tax information is correct
    filtered_location = Location.objects.filter(Q(id=location))
    if not filtered_location.exists():
        return False, "Este local No Existe, Able con el administrador"
    if not filtered_location[0].pre_tax_items == is_tax_included:
        return False, "La informacion de inpuestos/IVA proporcionada no coincide con nuetros records."
    
    if filtered_location[0].pre_tax_items:
        tax = filtered_location[0].local_tax/100 * grandTotal
        grandTotal = grandTotal + float_to_decimal(tax)

    if not grandTotal == float_to_decimal(data['grandTotal']):
        return False, "El total no coincide con el total proporcionada"
    # If the both prices match then  front end and back
    return True, ""
