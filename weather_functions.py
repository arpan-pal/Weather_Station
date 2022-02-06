'''
This file contains relevant functions I am using in this priject.
See weather_map.py for example.
'''

# functions defined in this file
__all__ = [
    'print_system_info',
    'update_quote',
]
import requests

def print_system_info(display):
    epd = display.epd

    print('System info:')
    print('  display size: {}x{}'.format(epd.width, epd.height))
    print('  img buffer address: {:X}'.format(epd.img_buf_address))
    print('  firmware version: {}'.format(epd.firmware_version))
    print('  LUT version: {}'.format(epd.lut_version))
    print()



def update_quote():
    quote_url = 'https://www.quotepub.com/api/widget/?type=qotd_t'
    quote_data = requests.get(quote_url).json()
    quote = "Your default quote goes here."
    max_len = 105
    if len(quote_data['quote_body']+quote_data['quote_author'])<max_len:
        quote = quote_data['quote_body']+' -'+quote_data['quote_author']
        return quote
    else:
        quote_url = 'https://www.quotepub.com/api/widget/?type=rand&limit=7'
        quote_data = requests.get(quote_url).json()
        for i in quote_data:
            if len(i['quote_body']+' -'+i['quote_author'])<max_len:
                quote = i['quote_body']+' -'+i['quote_author']
                return quote
    return quote
