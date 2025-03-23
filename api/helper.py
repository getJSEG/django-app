import random
import string
import decimal
from decimal import Decimal
import os
import requests
from django.db.models import Q
from django.conf import settings

countryCode = {
    'belize': '501',
    'guatemala': '502',
    'el salvador': '503',
    'honduras':'504',
    'nicaragua': '505',
    'costarica': '506',
    'panama': '507',
    'ecuador': '597',
    'colombia': '57',
    'mexico': '52',
    'united state': '1',
    'canada': '1',
}

locationType = {
    'RETAIL': '100',
    'WAREHOUSE': '200',
    'DISTRIBUTION_CENTER': '300'
}

# Generation Store Code
def store_number_generator(location_type, country):
    location_number = ''
    length = 6
    # get the location type
    # CHANGE THIS TO LOWER CASE
    for key, value in locationType.items():
        if location_type.upper() == key:
            location_number = value

    # get country code
    for key, value in countryCode.items():
        # CHANGE THIS TO LOWER CASE
        if country.lower() == key:
            location_number = location_number + value
    # create random number
    code = ''.join(random.choices(string.ascii_lowercase, k=length))
    # join the code and 
    location_number = location_number + str(code)
    
    return str(location_number)

# Generatino SKU Code
def generate_sku(name, brand, size, description, productId):
    sku = ''
    product_id_str = str(productId)

    try: 
        sku = sku + name[:5].strip().title()
        sku = sku + size[:3].strip().title()
        words = description.split()
        for word in  words:
            sku = sku + word[:4].strip().title()

        product_id = product_id_str[:8]
            
        sku = sku +  brand[:5] + product_id
    except: 
        return ''

    return ''.join(e for e in sku if e.isalnum())

#  Calculate the balance
def  cal_balance(grand_total, amount_paid): 
    balance = grand_total

    if amount_paid <= 0:
        return balance
    
    if amount_paid > 0:
        balance = balance - amount_paid

    return balance


#This Create pre signed url to upload imge in the front end
def generate_presign_url( account_id = settings.CLOUDFLARE_ACCOUNT_ID , api_token=settings.CLOUDFLARE_API_KEY):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v2/direct_upload"

    headers = { 
        "Authorization": f"Bearer {api_token}"
    }
    
    files = {
        "requireSignedURLs": False, # id this is true its secure else its public
    }

    response = requests.post(url, headers=headers, files=files)

    response.raise_for_status()

    return response.json()["result"]
















 # Search Model
# Check is date is grater that today date
# if not the call api to again to refresh the toke
# else use the same token.
def getWompiAuthentication():

    external_api_url = 'https://id.wompi.sv/connect/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = f"grant_type=client_credentials&client_id=48171e40-7b90-4f76-80a1-730833968370&client_secret=2b8f015e-8e37-467d-94fb-bcade95d1adb&audience=wompi_api"
    response =  requests.request('POST', external_api_url, headers=headers, data=payload)
    print(response)
    # print(response.status_code)
    # print(response.headers)
    # print(int(response.status_code) >= 400)

    if int(response.status_code) == 400:
        raise Exception('Something Went Wrong with the payment Please check with you Admin')
    if(int(response.status_code) > 401):
        raise Exception('Something Went Wrong Please check with you Admin')
    
    
    data = response.json()
    token = data.pop("access_token")
    # This Should be save to a model in the database
    # print(data.pop("access_token")) # token
    # print(data.pop("expires_in")) #Expiration
    # print(data.pop("token_type")) #token_type

    return token

    








def transcation3ds(token):

    external_api_url = 'https://id.wompi.sv/connect/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = f"grant_type=client_credentials&client_id={os.environ.get('WOMPI_API_ID')}&client_secret={os.environ.get('WOPMI_AP_SECRETE_KEY')}&audience=wompi_api"
    response =  requests.request('POST', external_api_url, headers=headers, data=payload)
    print(response)
    print(response.status_code)
    print(response.headers)
    print(int(response.status_code) >= 400)

    if int(response.status_code) == 400:
        raise Exception('Something Went Wrong with the payment Please check with you Admin')
    if(int(response.status_code) < 401):
        raise Exception('Something Went Wrong Please check with you Admin')
    
    
    data = response.json()
    token = data.pop("access_token")
        # This Should be save to a model in the database
        # print(data.pop("access_token")) # token
        # print(data.pop("expires_in")) #Expiration
        # print(data.pop("token_type")) #token_type

    return token
    # return Response({'client_secret': payment_intent['client_secret']})
    



def transactionPos(token):
    return



