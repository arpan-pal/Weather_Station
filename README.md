# Weather Station
Shows weather of two cities. Takes two zip codes and shows their current weather, 6 hours' forecast and next 3 days' forecast. It displays the weather data on a 7.8 inch e-paper display.

# Hardwares
This is one of my side projects. I have a Raspberry Pi 4. I bought a 7.8in e-paper display of waveshare and wrote this code. More on the display I used can be found here: https://www.waveshare.com/wiki/7.8inch_e-Paper_HAT and the actual display can be boght here: https://www.waveshare.com/product/displays/e-paper/7.8inch-e-paper.htm or https://www.waveshare.com/product/displays/e-paper/7.8inch-e-paper-hat.htm  or on Amazon.

# Drivers
Most importantly the display I am using is controled by the IC _IT8951_. I used the code from this Git repo: https://github.com/GregDMeyer/IT8951 to set up the interface and control it through python.


# Weather API
What it does is, it takes two zip codes as inputs and uses the python library uszipcode to find out the city name, State, and their corresponding lattitudes and longitudes. Then it uses the free openweathermap api to collect data form there. Check out here: https://openweathermap.org/api for more on that. It uses two type of calls, namely it does _weather_ call to get the current weather data and it uses  _onecall_ for getting the hourly forecast data. With free account openweathermap.org does not allow more than 1000 calls a day for the _onecall_ type api call, so becareful when you are playing around with it.

## Layout
By default the weather data and the screen refresh every 10 minutes and in case you lost your internet connection it shows the message _"Waiting for internet...'_ on the screen and checks back in every 30 seconds to see if it is online. In that case the screen layout looks like this:

---
<img src = "https://github.com/arpan-pal/Weather_Station/blob/main/weather_ofline.png?raw=true" width = "800" height = "600">

---

After it gets connected with the internet and fetches the weather data successfully, the screen layout remains the same but the blocks populates with weather information. Here is an example of the screen layout when the system is online:

---
<img src = "https://github.com/arpan-pal/Weather_Station/blob/main/weather_online.png?raw=true" width = "800" height = "600">

---

 

## Daily Quotes
I also used the narrow black band towards the bottom to display a quote of the day. By default it refresh every 12 hours. I used an api from https://www.quotepub.com/ for getting that. Look in the file _weather_functions.py_ for more details.

## Final Product

Finally, I have been able to get help from a friend of mine in the engineering department and he helped me design and 3D-print a case for the screen and the boards. Here is how the final product looks in the case:

---
<img src = "https://github.com/arpan-pal/Weather_Station/blob/main/FinalResult1.jpg?raw=true" width = "700" height = "500"> 

<img src = "https://github.com/arpan-pal/Weather_Station/blob/main/FinalResult2.jpg?raw=true" width = "700" height = "500">

---

## Coming soon...

I have made some further improvements to this and have added a temperature and humidity sensor to the weather station. So now I have access to the room temperature and himidity data and slightly changed the layout of the display to make room for displaying those data. I have the updated code for that and will update it the next chance I get to work on this fun project. 

Also I have a plan to set it up in a way so that every time I restart the Raspberry Pi, it syncs with the version of code present in the github. That way I'll be able to make changes and improvements remotely on the screen.



