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
import random

def print_system_info(display):
    epd = display.epd

    print('System info:')
    print('  display size: {}x{}'.format(epd.width, epd.height))
    print('  img buffer address: {:X}'.format(epd.img_buf_address))
    print('  firmware version: {}'.format(epd.firmware_version))
    print('  LUT version: {}'.format(epd.lut_version))
    print()



def update_quote():
    quote = "No suitable quote found today. Just wanted to remind you, Arpan loves you. ;)"
    #max_len = 105
    #quote = "No suitable quote found today. Just wanted to remind you, Arpan loves you. :)"

    max_len = 105 # Maximum length of a quote can be suitably displayed on the display

    k = 0
    while(k<7):
            file  = open('Quotes.txt')
            content = file.readlines()
            file.close()
            r = random.randint(0,len(content))
            if len(content[r].rstrip('\n'))> 1 and len(content[r].rstrip('\n')) < max_len:
                quote = content[r].rstrip('\n')
                break
            else:
                k+=1
                continue
    return quote
