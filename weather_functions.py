'''
This file contains relevant functions I am using in this priject.
See weather_map.py for example.
'''

# functions defined in this file
__all__ = [
    'print_system_info',
    'update_quote',
]
#import requests
import os
import random
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
openai_api_key = os.environ.get("OPENAI_API_KEY")

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
    max_len = 105 # Maximum length of a quote so that it can be suitably displayed on the display

    try:
        from openai import OpenAI
        k = 0
        while(k<3):
            client = OpenAI(api_key=openai_api_key)

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                    "role": "system",
                    "content": "You are my virtual daily quote generator."
                    },
                    {
                    "role": "user",
                    "content": "Pick a theme for today from the themes below:\nMotivation: Inspiring quotes to uplift and motivate your audience.\nSuccess: Quotes about achieving goals, overcoming obstacles, and reaching success.\nPositivity: Quotes focused on positivity, optimism, and gratitude.\nWisdom: Thought-provoking quotes offering wisdom, insights, and life lessons.\nCourage: Quotes about courage, resilience, and facing challenges head-on.\nGrowth: Quotes that encourage personal growth, self-improvement, and learning.\nHappiness: Quotes about finding joy, contentment, and happiness in life.\nLeadership: Inspirational quotes about leadership, influence, and making a difference.\nLove: Quotes about love, kindness, compassion, and relationships.\nCreativity: Quotes to spark creativity, innovation, and thinking outside the box.\n\nThen generate a creative, funny, and sarcastic quote for today.\nReturn a json with two keys, Theme and Quote, and nothing else."
                    },
                    ],
                temperature=0.9,
                max_tokens=500,
                #top_p=1,
                #frequency_penalty=0,
                #presence_penalty=0
            )
            if(len(json.loads(response.choices[0].message.content)['Quote'])) > 1 and len(json.loads(response.choices[0].message.content)['Quote']) < max_len:
                quote = json.loads(response.choices[0].message.content)['Quote']+'-AI'
                break
            else:
                k+=1
                continue
             
    except:
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
