from re import sub
from decimal import *


def normalize_price(price_str):
    return  Decimal(sub(r'[^\d.]', '', price_str))

def normalize_size(size_str):
    return  float(sub(r'[^\d.]', '', size_str))

def normalize_li_tags(tags):
    normalized_list = []
    for tag in tags:
        normalized_list.append(tag.text)
    return normalized_list

def normalize_address(full_address):
    street_name = 'N/A'
    street_number = 'N/A'

    splitted_address = full_address.split(',')
    state = splitted_address.pop() if splitted_address else 'N/A'
    town = splitted_address.pop() if splitted_address else 'N/A'
    settlement = splitted_address.pop() if splitted_address else 'N/A'
    full_street = splitted_address.pop() if splitted_address else None
    if full_street:
        full_street_list = full_street.split(' ')
        if len(full_street_list) > 1:
            if full_street_list[-1].isnumeric():
                street_number = full_street_list.pop()
                street_name = ' '.join(full_street_list)
            else:
                street_number = 'N/A'
                street_name = full_street
    else: 
        street_name = 'N/A'
        street_number = 'N/A'

    normalized_address = {
        "street_name": street_name.strip(),
        "street_number": street_number.strip(),
        "settlement": settlement.strip(),
        "town": town.strip(),
        "state": state.strip(),
        "country": "Mexico"
    }

    return normalized_address