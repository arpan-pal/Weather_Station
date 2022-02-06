'''
This file is the main file of this project. This takes zip codes of two cities as input, 
and then extracts informations about them like name of the city, state, lattitute and longitude.
Then it uses those information to extract weather data using the 'openweathermap' api.
Then it shows on the e-paper display in my designed layout along with a quote of the day.
Check out the image files 'weather_online.png', 'weather_ofline.png' and 'online_layout.png'
to find out the data displaying layout.
'''

import sys
import os, stat
import wget
import time
from PIL import Image,ImageDraw, ImageOps
import requests
import datetime
import uszipcode
from IT8951.display import AutoEPDDisplay, VirtualEPDDisplay
from IT8951 import constants
from weather_functions import *     # I wrote some helpful functions here. In future I plan to clean the code up and move some of the work as functions in this file.
from weather_fonts import *     # I just used this file to define some of the fonts along with their sizes I wanted. I ended up using only two fonts but you can use many more and make the project look much cooler.

# Zipcode of cities you are interested in. If you are not interested in two cities then repeat the same zipcode but do not leave one blank.
zip_1 = 77801
zip_2 = 77801

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





print('\nProcess started.\n')
epd = AutoEPDDisplay(vcom = -1.52, rotate = None, spi_hz=60000000)
print_system_info(epd)
epd.clear()

#loading and processing different weather icons
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

while(True):
    try:
        weather_draw.rectangle((0,400,width,460), fill = 0) # Narrow black band below current weather tab, separating it from hourly forecast
        weather_draw.rectangle((0,970,width,1030), fill = 0) # Narrow black band below hourly forecast tab, separating it from daily forecast
        
        
        white_mask = Image.new("L",(w2-10,290), 255) #Creating a white mask for the current weather tabs
        weather_image.paste(white_mask,(5,115))
        weather_image.paste(therm_img,(0,115))
        weather_draw.text((440,125),'Feels like:',font = sans_it60, fill=0)
        weather_image.paste(wind_img, (0,270))
        
        
        weather_image.paste(white_mask,(w2+5,115))
        weather_image.paste(therm_img,(5+w2,115))
        weather_draw.text((w2+440,125),'Feels like:',font = sans_it60, fill=0)
        weather_image.paste(wind_img, (5+w2,270))
        
        white_mask = Image.new("L", (w2-10,500), 255)   #Creating a white mask for the hourly forecast tabs
        weather_image.paste(white_mask, (5,465))
        weather_image.paste(white_mask, (5+w2,465))
        
        white_mask = Image.new("L", (w2-10,500), 255)   #Creating a white mask for the daily forecast tabs
        weather_image.paste(white_mask, (5,1040))
        weather_image.paste(white_mask, (5+w2,1040))   
        
        weather_draw.rectangle((w2-325,height-70,w2+325,height), fill=0) #Bottom rectangle for showing last update time
        
        
        
        
        print("\n\nUpdating frist city's weather...\n")
        
        forecast_url = "http://api.openweathermap.org/data/2.5/onecall?lat="+lat_1
        forecast_url+= "&lon="+lng_1+"&exclude=minutely,current,alerts&units=imperial&appid="
        forecast_url+= api_key_forecast
        
        current_url = "http://api.openweathermap.org/data/2.5/weather?zip=%d&units=imperial&id=524901&appid="%(zip_1)
        current_url+= api_key_current
        
        weather_forecast_1 = requests.get(forecast_url).json()
        weather_now_1 = requests.get(current_url).json()
        
        print('\nUpdating hourly forecast...\n')
        count = 0
        for i in weather_forecast_1['hourly']:
            if i['dt'] > time.time()+600:
                i['temp'] = '%d'%(round(i['temp']))
                i['temp'] = i['temp']+u"\N{DEGREE SIGN}"+'F'
                i['feels_like'] = '%d'%(round(i['feels_like']))
                i['feels_like'] = i['feels_like']+u"\N{DEGREE SIGN}"+'F'
                icon_size = 110
                try:
                    icon_img = Image.open(i['weather'][0]['icon']+'@2x.png')
                    print('    Image available locally.')
                except:
                    print('    Image not available locally. Downloading from the web.')
                    icon_url = 'http://openweathermap.org/img/wn/'+i['weather'][0]['icon']+'@2x.png'
                    icon = wget.download(icon_url)
                    icon_img = Image.open(icon)
                
                icon_img = icon_img.crop((10,10,90,90))
                icon_img = icon_img.resize((icon_size,icon_size))
                icon_img = icon_img.convert('L')
                icon_img = ImageOps.invert(icon_img)
                time_then = datetime.datetime.fromtimestamp(i['dt']).strftime('%I %p')
                weather_draw.text((10+320*(count%3),480+270*(count//3)),time_then,font = sans40,fill=0)
                weather_image.paste(icon_img,(10+320*(count%3),520+270*(count//3)))
                weather_draw.text((10+320*(count%3),520+270*(count//3)+icon_size+5),i['weather'][0]['main'],font = sans40,fill=0)
                weather_draw.text((10+320*(count%3)+icon_size+5,520+270*(count//3)+(icon_size/2)+10),'RF: '+i['feels_like'],font = serif_it40,fill=0)
                weather_draw.text((10+320*(count%3)+icon_size+5,520+270*(count//3)+(icon_size/2)-70),i['temp'],font = serif60,fill=0)
                count+=1
            if count == 6:
                print('\nHourly forecast update complete.\n')
                break
        
        print('\nUpdating daily forecast...\n')
        count = 0
        for i in weather_forecast_1['daily']:
            if i['dt'] > time.time()+43800:
                temp_max = '%d'%(round(i['temp']['max']))
                temp_max+= u"\N{DEGREE SIGN}"+'F'
                temp_min = '%d'%(round(i['temp']['min']))
                temp_min+= u"\N{DEGREE SIGN}"+'F'
                date_then = datetime.datetime.fromtimestamp(i['dt']).strftime('%m/%d')
                icon_size = 120
                try:
                    icon_img = Image.open(i['weather'][0]['icon']+'@2x.png')
                    print('    Image available locally.')
                except:
                    print('    Image not available locally. Downloading from the web.')
                    icon_url = 'http://openweathermap.org/img/wn/'+i['weather'][0]['icon']+'@2x.png'
                    icon = wget.download(icon_url)
                    icon_img = Image.open(icon)
                    icon_img = icon_img.crop((10,10,90,90))
                icon_img = icon_img.resize((icon_size,icon_size))
                icon_img = icon_img.convert('L')
                icon_img = ImageOps.invert(icon_img)
                weather_draw.text((10+330*(count%3),1100-50),date_then,font = serif40,fill=0)
                weather_image.paste(icon_img,(5+330*(count%3),1100))
                weather_draw.text((10+330*(count%3),1100+icon_size+10),i['weather'][0]['main'],font = serif40,fill=0)
                weather_draw.text((15+330*(count%3)+icon_size,1100),temp_max,font = serif40,fill=0)
                weather_draw.text((15+330*(count%3)+icon_size,1100+70),temp_min,font = serif40,fill=0)
                count+=1
            if count == 3:
                print('\nDaily forecast update complete.\n')
                break
                    
                    
        print('\nUpdating currnet weather...\n')
        temp_now_1 = '%d'%(round(weather_now_1['main']['temp']))
        temp_now_1+= u"\N{DEGREE SIGN}"+'F'
        
        temp_max_1 = '%d'%(round(weather_now_1['main']['temp_max']))
        temp_max_1+= u"\N{DEGREE SIGN}"+'F'
        temp_min_1 = '%d'%(round(weather_now_1['main']['temp_min']))
        temp_min_1+= u"\N{DEGREE SIGN}"+'F'
        
        feels_like_1 = '%d'%(round(weather_now_1['main']['feels_like']))
        feels_like_1+=u"\N{DEGREE SIGN}"+'F'
        wind_1 = '%d'%(round(weather_now_1['wind']['speed']))
        humid_1 = '%d'%weather_now_1['main']['humidity']
        main_description_1 = weather_now_1['weather'][0]['main']
        description_1 = weather_now_1['weather'][0]['description']
        weather_draw.text((160,130),temp_now_1,font = serif80,fill = 0)
        weather_draw.text((730,120),feels_like_1,font = serif80,fill = 0)
        weather_draw.text((160,270),wind_1,font = serif80,fill = 0)
        weather_draw.text((270,290),'mph',font = serif40,fill = 0)
        try:
            icon_img = Image.open(weather_now_1['weather'][0]['icon']+'@2x.png')
            print('    Image available locally.')
        except:
            print('    Image not available locally. Downloading from the web...')
            icon_url = 'http://openweathermap.org/img/wn/'+weather_now_1['weather'][0]['icon']+'@2x.png'
            icon = wget.download(icon_url)
            icon_img = Image.open(icon)
        
        icon_img = icon_img.crop((10,10,90,90))
        icon_img = icon_img.resize((200,200))
        icon_img = icon_img.convert('L')
        icon_img = ImageOps.invert(icon_img)
        weather_image.paste(icon_img,(380,200))
        weather_draw.text((580,250),main_description_1,font = serif60, fill = 0)
        weather_draw.text((650,350),'Humidity: '+humid_1+'%',font = sans_it40, fill = 50)
        weather_draw.text((10,410),'Max: '+temp_max_1+'   Min: '+temp_min_1+',   '+description_1, font = sans40, fill = 255)
        print('\nCurrent weather update complete.\n')
        
        print("\nFrist city's weather update complete.\n\n")
            
            
        
        
        print("\n\nUpdating second city's weather...\n")
        
        forecast_url = "http://api.openweathermap.org/data/2.5/onecall?lat="+lat_2
        forecast_url+= "&lon="+lng_2+"&exclude=minutely,current,alerts&units=imperial&appid="
        forecast_url+= api_key_forecast
        
        current_url = "http://api.openweathermap.org/data/2.5/weather?zip=%d&units=imperial&id=524901&appid="%(zip_2)
        current_url+= api_key_current
        
        weather_forecast_2 = requests.get(forecast_url).json()
        weather_now_2 = requests.get(current_url).json()
        print('\nUpdating hourly forecast...\n')
        count = 0
        for i in weather_forecast_2['hourly']:
            if i['dt'] > time.time()+600:
                i['temp'] = '%d'%(round(i['temp']))
                i['temp'] = i['temp']+u"\N{DEGREE SIGN}"+'F'
                i['feels_like'] = '%d'%(round(i['feels_like']))
                i['feels_like'] = i['feels_like']+u"\N{DEGREE SIGN}"+'F'
                icon_size = 110
                try:
                    icon_img = Image.open(i['weather'][0]['icon']+'@2x.png')
                    print('    Image available locally.')
                except:
                    print('    Image not available locally. Downloading from the web...')
                    icon_url = 'http://openweathermap.org/img/wn/'+i['weather'][0]['icon']+'@2x.png'
                    icon = wget.download(icon_url)
                    icon_img = Image.open(icon)
                
                icon_img = icon_img.crop((10,10,90,90))
                icon_img = icon_img.resize((icon_size,icon_size))
                icon_img = icon_img.convert('L')
                icon_img = ImageOps.invert(icon_img)
                time_then = datetime.datetime.fromtimestamp(i['dt']).strftime('%I %p')
                weather_draw.text((10+320*(count%3)+w2,480+270*(count//3)),time_then,font = sans40,fill=0)
                weather_image.paste(icon_img,(10+320*(count%3)+w2,520+270*(count//3)))
                weather_draw.text((10+320*(count%3)+w2,520+270*(count//3)+icon_size+5),i['weather'][0]['main'],font = sans40,fill=0)
                weather_draw.text((10+320*(count%3)+w2+icon_size+5,520+270*(count//3)+(icon_size/2)+10),'RF: '+i['feels_like'],font = serif_it40,fill=0)
                weather_draw.text((10+320*(count%3)+w2+icon_size+5,520+270*(count//3)+(icon_size/2)-70),i['temp'],font = serif60,fill=0)
            
                count+=1
            if count == 6:
                print('\nHourly forecast update complete.\n')
                break
            
        print('\nUpdating daily forecast...\n')
        count = 0
        for i in weather_forecast_2['daily']:
            if i['dt'] > time.time()+43800:
                temp_max = '%d'%(round(i['temp']['max']))
                temp_max+= u"\N{DEGREE SIGN}"+'F'
                temp_min = '%d'%(round(i['temp']['min']))
                temp_min+= u"\N{DEGREE SIGN}"+'F'
                date_then = datetime.datetime.fromtimestamp(i['dt']).strftime('%m/%d')
                icon_size = 120
                try:
                    icon_img = Image.open(i['weather'][0]['icon']+'@2x.png')
                    print('    Image available locally.')
                except:
                    print('    Image not available locally. Downloading from the web.')
                    icon_url = 'http://openweathermap.org/img/wn/'+i['weather'][0]['icon']+'@2x.png'
                    icon = wget.download(icon_url)
                    icon_img = Image.open(icon)
                    icon_img = icon_img.crop((10,10,90,90))
                icon_img = icon_img.resize((icon_size,icon_size))
                icon_img = icon_img.convert('L')
                icon_img = ImageOps.invert(icon_img)
                weather_draw.text((15+330*(count%3)+w2,1100-50),date_then,font = serif40,fill=0)
                weather_image.paste(icon_img,(10+330*(count%3)+w2,1100))
                weather_draw.text((15+330*(count%3)+w2,1100+icon_size+10),i['weather'][0]['main'],font = serif40,fill=0)
                weather_draw.text((20+330*(count%3)+icon_size+w2,1100),temp_max,font = serif40,fill=0)
                weather_draw.text((20+330*(count%3)+icon_size+w2,1100+70),temp_min,font = serif40,fill=0)
                count+=1
            if count == 3:
                print('\nDaily forecast update complete.\n')
                break
            
        print('\nUpdating currnet weather...\n')
        temp_now_2 = '%d'%(round(weather_now_2['main']['temp']))
        temp_now_2+= u"\N{DEGREE SIGN}"+'F'
        
        temp_max_2 = '%d'%(round(weather_now_2['main']['temp_max']))
        temp_max_2+= u"\N{DEGREE SIGN}"+'F'
        temp_min_2 = '%d'%(round(weather_now_2['main']['temp_min']))
        temp_min_2+= u"\N{DEGREE SIGN}"+'F'
        
        feels_like_2 = '%d'%(round(weather_now_2['main']['feels_like']))
        feels_like_2+=u"\N{DEGREE SIGN}"+'F'
        wind_2 = '%d'%(round(weather_now_2['wind']['speed']))
        humid_2 = '%d'%weather_now_2['main']['humidity']
        main_description_2 = weather_now_2['weather'][0]['main']
        description_2 = weather_now_2['weather'][0]['description']
        
        weather_draw.text((160+w2,130),temp_now_2,font = serif80,fill = 0)
        weather_draw.text((730+w2,120),feels_like_2,font = serif80,fill = 0)
        weather_draw.text((160+w2,270),wind_2,font = serif80,fill = 0)
        weather_draw.text((270+w2,290),'mph',font = serif40,fill = 0)
        try:
            icon_img = Image.open(weather_now_2['weather'][0]['icon']+'@2x.png')
            print('    Image available locally.')
        except:
            print('    Image not available locally. Downloading from the web...')
            icon_url = 'http://openweathermap.org/img/wn/'+weather_now_2['weather'][0]['icon']+'@2x.png'
            icon = wget.download(icon_url)
            icon_img = Image.open(icon)
        
        icon_img = icon_img.crop((10,10,90,90))
        icon_img = icon_img.resize((200,200))
        icon_img = icon_img.convert('L')
        icon_img = ImageOps.invert(icon_img)
        weather_image.paste(icon_img,(380+w2,200))
        weather_draw.text((580+w2,250),main_description_2,font = serif60, fill = 0)
        weather_draw.text((w2+650,350),'Humidity: '+humid_2+'%',font = sans_it40, fill = 50)
        weather_draw.text((10+w2,410),'Max: '+temp_max_2+'   Min: '+temp_min_2+',   '+description_2, font = sans40, fill = 255)
        print('\nCurrent weather update complete.\n')
        print("\nSecond city's weather update complete.\n\n")
        
        
        # The quote updates every 12 hours.
        if quote_update_time+43200 < time.time():
            quote = update_quote()
            quote_update_time = time.time()
        
        weather_draw.text((5,980), quote, font = serif_it40, fill = 255)    # Writing the quote
            
            
        update_time = 'Last updated: '+time.strftime('%I:%M %p')
        date_now = time.strftime('%m/%d/%Y')
        date_now = date_now[:-4]+date_now[-2:]
        
        weather_draw.text((w2-300,height-55),update_time+',  '+date_now, font = sans40, fill = 255)
        
        '''if save_online_image == 1:
            weather_image.save('weather_online.png')    # Saving the image which is generated when when the system is online and the weather is being displayed
            os.chmod('weather_online.png',stat.S_IRWXG | stat.S_IRWXO | stat.S_IRWXU)      # Changing the default permission and granting permission to all users
            save_online_image = 0'''
        
        epd.frame_buf.paste(weather_image, (0,0))   # Showing weather image on the screen with partial update
        epd.draw_partial(constants.DisplayModes.GL16)
        print('\nOne iteration complete. Last updated:'+update_time+', '+date_now)
        time.sleep(600)
    except:
        #This will print the message 'Waiting for internet...' on the display. If some error occours by default it'll assume that the internet is not connected and so will show this message.
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
            
        epd.frame_buf.paste(weather_image, (0,0))   # Showing ofline weather image on the screen with partial update
        epd.draw_partial(constants.DisplayModes.GL16)
        time.sleep(30)      # Will check again after 30 seconds to see if the internet is connected or not.

