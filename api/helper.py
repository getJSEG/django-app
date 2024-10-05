import random
import string

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


def generate_sku(name,brand, size, description, productId):
    sku = ''
    product_id_str = str(productId)

    try: 
        sku = sku + name[:5].strip().title()
        sku = sku + size[:3].strip().title()
        words = description.split()
        for word in  words:
            sku = sku + word[:4].title().strip()

        product_id = product_id_str[:8]
            
        sku = sku +  brand[:5] + product_id
    except: 
        return ''

    return ''.join(e for e in sku if e.isalnum())



def  cal_balance(grand_total, amount_paid): 
    balance = grand_total

    if amount_paid <= 0:
        return balance
    
    if amount_paid > 0:
        balance = balance - amount_paid

    return balance