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

def generate_store_number(location_type, country):
    location_number = ''
    length = 6
    # get the location type
    # CHANGE THIS TO LOWER CASE
    for key, value in locationType.items():
        if location_type == key:
            location_number = value

    # get country code
    for key, value in countryCode.items():
        # CHANGE THIS TO LOWER CASE
        if country == key:
            location_number = location_number + value
    # create random number
    code = ''.join(random.choices(string.ascii_lowercase, k=length))
    # join the code and 
    location_number = location_number + str(code)

    return str(location_number)

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smpt.gmail.com'
# EMAIL_HOST_USER = '@gmail.com'
# EMAIL_HOST_PASSWORD = 'password here'
# EMAIL_PORT = 587
