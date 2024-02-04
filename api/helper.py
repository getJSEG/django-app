import random

countryCode = {
    'belize': 501,
    'guatemala': 502,
    'el salvador': 503,
    'honduras':504,
    'nicaragua': 505,
    'costarica': 506,
    'panama': 507,
    'ecuador': 597,
    'colombia': 57,
    'mexico': 52,
    'united state': 1,
    'canada': 1,
}

locationType = {
    'store': 100,
    'wharehouse': 200
}

def generate_location_id(location_type, country):
    location_number = ''
    length = 6
    # get the location type
    for key, value in locationType.items():
        if location_type == key:
            location_number = value
    # get country code
    for key, value in countryCode.items():
        if country == key:
            location_number = location_number + value
    # create random number
    code = random.choices(k=length)
    # join the code and 
    location_number = location_number + code

    return str(location_number)

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smpt.gmail.com'
# EMAIL_HOST_USER = '@gmail.com'
# EMAIL_HOST_PASSWORD = 'password here'
# EMAIL_PORT = 587
