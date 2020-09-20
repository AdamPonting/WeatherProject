# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 16:19:02 2020
Local Info Web Scraping Project
@author: Adam ponting's pc
"""
import requests

from bs4 import BeautifulSoup

url = 'https://www.bbc.co.uk/weather/2650225'
page = requests.get(url)
page_html = page.text

soup = BeautifulSoup(page_html, features = "lxml")

"""
Explained (next 2 lines)
- Searches for the location name, based on a h1 id. Splits it in two and uses the first string
- Searches for todays temperature, based on a span class.
"""
locationName = ((soup.find("h1", attrs={'id': 'wr-location-name-id'}).text).split(" - "))[0]
todaysTemp = (soup.find("span", attrs={'class': 'wr-value--temperature--c'}).text)

"""
Explained (next 4 lines)
- Searches for each individual time, based on span class, splitting each one by comma.
- Searches for each individual temperature, based on div class, splitting each one by space to seperate Celsius and Farenheit.
[0] is used to only add Celsius.
- Searches for each individual rain chance stat, based on div class, splitting each one by space (mass info) then by c (attached descriptor aka 'c'hance) as previously ^.
- Searches for each individual wind speed, retrieving just the numeric mph speed by splitting the mass information as previously ^.
"""
todaysTimes = [temp.text for temp in soup.find_all("span", attrs={'class': 'wr-time-slot-primary__time'})]
todaysTemps = [temp.text.split(" ")[0] for temp in soup.find_all("div", attrs={'class': 'wr-time-slot-primary__temperature'})]
todaysRainChance = [temp.text.split("c")[0] for temp in soup.find_all("div",attrs={'class': 'wr-u-font-weight-500'})]
todaysWinds = [temp.text.split(" ")[1].split("d")[1] for temp in soup.find_all("div", attrs={'class': 'wr-time-slot-primary__wind-speed'})]

spacing = ["  ", "", "          "]

print("BBC Weather " + locationName)
print("Todays Average Temperature: " + todaysTemp)
print("Time   Temp  RainChance  WindSpeed")
index = 0
for time in todaysTimes:
    """
    Explained (next 8 lines): deals with spacing differences that depend
    on the size of todaysTemps & todaysRainChance.
    """
    if(len(todaysTemps[index]) > 2):
        spacing[1] = "   "
    else:
        spacing[1] = "    "
    if(len(todaysRainChance[index]) > 2):
        spacing[2] = "         "
    else:
        spacing[2] = "          "
        
    print(time + spacing[0] + todaysTemps[index] + spacing[1] + todaysRainChance[index] + spacing[2] + todaysWinds[index] + "mph")
    index += 1
