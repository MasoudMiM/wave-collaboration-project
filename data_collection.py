# This is the code for data collection from the link shapred
# here is the link: https://onedrive.live.com/?authkey=%21AMogwvv2lAznbkw&id=94C083E5EBACF1E%214270&cid=094C083E5EBACF1E

# the page includes the folders with following name convention:
# Standard_Met_[station name]

# station names are:
# 41010 - page: https://www.ndbc.noaa.gov/station_page.php?station=41010
# 41043 - page: https://www.ndbc.noaa.gov/station_page.php?station=41043
# 41046 - page: https://www.ndbc.noaa.gov/station_page.php?station=41046
# 41047 - page: https://www.ndbc.noaa.gov/station_page.php?station=41047
# 41048 - page: https://www.ndbc.noaa.gov/station_page.php?station=41048
# 42056 - page: https://www.ndbc.noaa.gov/station_page.php?station=42056
# 42057 - page: https://www.ndbc.noaa.gov/station_page.php?station=42057
# 42058 - page: https://www.ndbc.noaa.gov/station_page.php?station=42058
# 42059 - page: https://www.ndbc.noaa.gov/station_page.php?station=42059
# 42060 - page: https://www.ndbc.noaa.gov/station_page.php?station=42060

# we will use the following libraries
import pandas as pd
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
import re
import urllib
import folium

# let's first read the coordinates of each station from the corresponding page
# they are tipycally shown in the page as: [] N [] W ([]] N [] W)
# as an example: 28.878 N 78.485 W (28°52'39" N 78°29'6" W)

# reading the page for station 41010:
# url = 'https://www.ndbc.noaa.gov/station_page.php?station=41010'
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')
# # let's find the coordinates with XPath: /html/body/div/main/section[1]/div/div[1]/p[1]/b[4]
# # the coordinates are in the 4th bold text
# coordinates = soup.find_all('b')[4].get_text()
# # let's extract the coordinates
# lat = re.findall(r'(\d+\.\d+) N', coordinates)
# lon = re.findall(r'(\d+\.\d+) W', coordinates)
# # let's print the coordinates
# print('The coordinates for station 41010 are: ', lat, lon)

# now let's create a for-loop to read the coordinates for all the stations
# we will store the coordinates in a dictionary
stations = ['41010', '41043', '41046', '41047', '41048', '42056', '42057', '42058', '42059', '42060']
coordinates = {}
for station in stations:
    url = 'https://www.ndbc.noaa.gov/station_page.php?station=' + station
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # let's find the coordinates with XPath: /html/body/div/main/section[1]/div/div[1]/p[1]/b[4]
    # the coordinates are in the 4th bold text
    coordinates_station = soup.find_all('b')[4].get_text()
    # let's extract the coordinates for each station and then put them in the dictionary
    lat = re.findall(r'(\d+\.\d+) N', coordinates_station)
    lon = re.findall(r'(\d+\.\d+) W', coordinates_station)
    # let's put the coordinates in the dictionary for each station
    coordinates[station] = [lat, lon]
    
# now, let's create a map and put these coordinates in the map
# let's create a map
map = folium.Map(location=[28.878, -78.485], zoom_start=6)
# let's add the markers for each station
for station in coordinates:
    folium.Marker([float(coordinates[station][0][0]), -float(coordinates[station][1][0])], popup=station).add_to(map)

# let's show the map
map.save('stations.html')
