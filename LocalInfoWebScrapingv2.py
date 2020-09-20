# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 16:19:02 2020
Local Info Web Scraping Project v2 OOProgramming
@author: Adam ponting's pc
"""
import requests
from bs4 import BeautifulSoup

def getSoup(url):
    return BeautifulSoup(requests.get(url).text, features = "lxml")


def getBBCInfoMain(soup):
    """
    Explained (next 2 lines)
    - Searches for the location name, based on a h1 id. Splits it in two and uses the first string
    - Searches for todays temperature, based on a span class.
    """
    locationName = ((soup.find("h1", attrs={'id': 'wr-location-name-id'}).text).split(" - "))[0]
    todaysTemp = (soup.find("span", attrs={'class': 'wr-value--temperature--c'}).text)
    return [locationName, todaysTemp]


def getBBCInfoChart(soup):
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
    return [todaysTimes, todaysTemps, todaysRainChance, todaysWinds]


def printBBCInfo(soup, infoMain, infoChart):    
    spacing = ["  ", "", "          "]

    print("BBC Weather " + infoMain[0])
    print("Todays Average Temperature: " + infoMain[1])
    print("Time   Temp  RainChance  WindSpeed")
    index = 0
    for time in infoChart[0]:
        """
        Explained (next 8 lines): deals with spacing differences that depend
        on the size of todaysTemps & todaysRainChance.
        """
        if(len(infoChart[1][index]) > 2):
            spacing[1] = "   "
        else:
            spacing[1] = "    "
        if(len(infoChart[2][index]) > 2):
            spacing[2] = "         "
        else:
            spacing[2] = "          "
        
        print(time + spacing[0] + infoChart[1][index] + spacing[1] + infoChart[2][index] + spacing[2] + infoChart[3][index] + "mph")
        index += 1

soup = getSoup('https://www.bbc.co.uk/weather/2650225')
printBBCInfo(soup,getBBCInfoMain(soup),getBBCInfoChart(soup))