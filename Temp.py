import sys
import os, stat
import wget
import time
from PIL import Image,ImageDraw, ImageOps
import requests
import datetime
import uszipcode
#from IT8951.display import AutoEPDDisplay, VirtualEPDDisplay
#from IT8951 import constants
from weather_functions import *     # I wrote some helpful functions here. In future I plan to clean the code up and move some of the work as functions in this file.
from weather_fonts import *


zip_1 = 77801
zip_2 = 77809

api_key_current = ""        # Your API Key
api_key_forecast = ""       # Your API Key for the onecall api. This is little delicate. If you have a free account then they'll not let you call the onecall API more than 1000 times in 24 hours. Both the keys can be same.

#Extracting information from zip_1
search = uszipcode.SearchEngine()
zip_info_1 = search.by_zipcode('%d'%zip_1).to_dict()
state_1 = zip_info_1['state']
city_1 = zip_info_1['major_city']
lat_1 = str(zip_info_1['lat'])
lng_1 = str(zip_info_1['lng'])

#Extracting information from zip_2
zip_info_2 = search.by_zipcode('%d'%zip_2).to_dict()
state_2 = zip_info_2['state']
city_2 = zip_info_2['major_city']
lat_2 = str(zip_info_2['lat'])
lng_2 = str(zip_info_2['lng'])

therm_img = Image.open('thermometer.png')
therm_img.load()
therm_img = therm_img.resize((200,200))
therm_img = therm_img.crop((30,30,170,170))
wind_img = Image.open('wind_1.png')
wind_img.load()
wind_img = wind_img.resize((120,120))


# Creating the layout
width,height= epd.width,epd.height
w2 = int(width/2)
epd.frame_buf.paste(0xFF, box=(0, 0, width, height))
weather_image = Image.new('L', (width,height), 255)
weather_draw = ImageDraw.Draw(weather_image)
weather_draw.line((0,110,width,110), width=6,fill=0)    # Top row for city names
weather_draw.line((w2,0,w2,height-70), fill = 0, width = 6)     # Dividor line at the middle between two city columns
weather_draw.rectangle((w2-325,height-70,w2+325,height), fill=0)    #Bottom rectangle for showing last update time
weather_draw.rectangle((0,400,width,460), fill = 0)     # Narrow black band below current weather tab, separating it from hourly forecast
weather_draw.rectangle((0,970,width,1030), fill = 0)    # Narrow black band below hourly forecast tab, separating it from daily forecast
weather_image.paste(therm_img,(0,115))
weather_draw.text((440,125),'Feels like:',font = sans_it60, fill=0)
weather_image.paste(wind_img, (0,270))
weather_image.paste(therm_img,(5+w2,115))
weather_draw.text((w2+440,125),'Feels like:',font = sans_it60, fill=0)
weather_image.paste(wind_img, (5+w2,270))


# Filling in the information for zip_1
weather_draw.text((60,10),city_1+','+state_1, font=sans_bold80,fill=10)

# Filling in the information for zip_2
weather_draw.text((width//2+60,10),city_2+','+state_2, font=sans_bold80,fill=10)


#weather_image.save('online_layout.png')    # Saving the layout image when the system would be online
#os.chmod('online_layout.png',stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)      # Changing the default permission and granting permission to all users

epd.frame_buf.paste(weather_image, (0,0))
epd.draw_full(constants.DisplayModes.GL16)
quote = "Your default quote goes here"
quote_update_time = 0
#save_online_image = 1      # Indicator variable whether to save the image when the system is online and the weather data is being displayed.
#save_ofline_image = 1      # Indicator variable whether to save the image when the system is ofline and the weather data is not being displayed.
print('\n\n\nStarting the weather update.')



print('\nCould not connect to the internet.\n')
white_mask = Image.new("L",(w2-10,290), 255) #Creating a white mask for the current weather tabs
weather_image.paste(white_mask,(5,115))
weather_image.paste(white_mask,(w2+5,115))
white_mask = Image.new("L", (w2-10,500), 255)   #Creating a white mask for the hourly forecast tabs
weather_image.paste(white_mask, (5,465))
weather_image.paste(white_mask, (5+w2,465))
white_mask = Image.new("L", (w2-10,500), 255)   #Creating a white mask for the daily forecast tabs
weather_image.paste(white_mask, (5,1040))
weather_image.paste(white_mask, (5+w2,1040))   

weather_draw.text((10,220),'Waiting for internet...',font = sans_it60,fill = 0)
weather_draw.text((10+w2,220),'Waiting for internet...',font = sans_it60,fill = 0)
weather_draw.text((10,730),'Waiting for internet...',font = sans_it60,fill = 0)
weather_draw.text((10+w2,730),'Waiting for internet...',font = sans_it60,fill = 0)
weather_draw.text((10,1200),'Waiting for internet...',font = sans_it60,fill = 0)
weather_draw.text((10+w2,1200),'Waiting for internet...',font = sans_it60,fill = 0)
weather_draw.rectangle((w2-325,height-70,w2+325,height), fill=0) #Bottom rectangle for showing last update time

weather_draw.text((5,980), quote, font = serif_it40, fill = 255)    # Writing the quote

'''if save_ofline_image == 1:
    weather_image.save('weather_ofline.png')    # Saving the image which is generated when when the system is ofline and the weather is not being displayed
    os.chmod('weather_ofline.png',stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)      # Changing the default permission and granting permission to all users
    save_ofline_image = 0'''
weather_image.save('weather_ofline.png')
