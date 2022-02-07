# Weather-EPD_7.8in
Shows weather of two cities. Takes two zip codes and shows their current weather, 6 hours' forecast and next 3 days' forecast.

# Hardwares
This is one of my side projects. I have a Raspberry Pi 4. I bought a 7.8in e-paper display of waveshare and wrote this code. More on the display I used can be found here: https://www.waveshare.com/wiki/7.8inch_e-Paper_HAT and the actual display can be boght here: https://www.waveshare.com/product/displays/e-paper/7.8inch-e-paper.htm or https://www.waveshare.com/product/displays/e-paper/7.8inch-e-paper-hat.htm  or on Amazon.

# Weather API
What it does is, it takes two zip codes as inputs and uses the python library uszipcode to find out the city name, State, and their corresponding lattitudes and longitudes. Then it uses the free openweathermap api to collect data form there. Check out here: https://openweathermap.org/api for more on that. It uses two type of calls, namely it does _weather_ call to get the current weather data and it uses  _onecall_ for getting the hourly forecast data. With free account openweathermap.org does not allow more than 1000 calls a day for the _onecall_ type api call, so becareful when you are playing around with it.

## Layout
By default ther weather data and the screen refresh every 10 minutes and in case you lost your internet connection it shows the message _"Waiting for internet...'_ on the screen and checks back in every 30 seconds to see if it is online. Check out the images 'weather_online.png', 'weather_ofline.png' and 'online_layout.png' to get more information on how the data and messages are displayed. To get an idea how it looks on the actual display I have uploaded an actual photo of my e-paper display. Check out the file 'RPI_Weather_EPD.jpg'.

## Daily Quotes
I also used the narrow black band towards the bottom to display a quote of the day. By default it refresh every 12 hours. I used an api from https://www.quotepub.com/ for getting that. Look in the file _weather_functions.py_ for more details.
## Drivers
Lastly and most importantly the display I am using is controled by the IC _IT8951_. I used the code from this Git repo: https://github.com/GregDMeyer/IT8951 to set up the interface and control it through python.
