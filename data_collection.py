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

# let's also add a logger to the code to keep track of the progress
# i want the logger to print the log in the console and also save it in a log file
import logging
import datetime

# create a log file with the current date and time
log_file = datetime.datetime.now().strftime('log_%Y-%m-%d_%H-%M-%S.log')

# create a logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(log_file),
                              logging.StreamHandler()])

LOGGER = logging.getLogger(__name__)

# creating a for-loop to read the coordinates for all the stations
# we will store the coordinates in a dictionary
stations = ['41010', '41043', '41046', '41047', '41048', '42056', '42057', '42058', '42059', '42060']
coordinates = {}
LOGGER.info('Start reading the coordinates for each station')
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
LOGGER.info('Creating a map to show the location of each station')
map = folium.Map(location=[28.878, -78.485], zoom_start=6)
# let's add the markers for each station
for station in coordinates:
    folium.Marker([float(coordinates[station][0][0]), -float(coordinates[station][1][0])], popup=station).add_to(map)

# let's show the map
LOGGER.info('Saving the map')
map.save('stations.html')

# let's create a folder to save the data
LOGGER.info('Creating a folder to save the data')
folder = 'data'
if not os.path.exists(folder):
    os.makedirs(folder)

# data is stored in folder /data and subfolders Standard_Met_[station name].
# within each subfolder, there are files with the following name convention: [station name]hYYYY.txt
# let's read this data and store it in a dictionary

# let's create a dictionary to store the data
LOGGER.info(f'Reading the data for each station from the folder {folder}')
data = {}
# let's read the data for each station
for station in stations:
    # let's create a subfolder for each station
    subfolder = folder + '/Standard_Met_' + station
    if not os.path.exists(subfolder):
        raise ValueError('The subfolder ' + subfolder + ' does not exist')
    # let's read the files for each station
    files = os.listdir(subfolder)
    # let's create a dictionary for each station
    data[station] = {}
    for file in files:
        LOGGER.info(f'Reading the file {file} for the station {station}')
        # let's read the data from the file
        data[station][file] = pd.read_csv(subfolder + '/' + file, skiprows=2 ,delim_whitespace=True, na_values=[999.0, 99.0]) #, parse_dates={'datetime': ['#YY', 'MM', 'DD', 'hh']})
        # let's save the data in a csv file - first strip the file extension
        file_name = file.split('.')[0]
        data[station][file].to_csv(subfolder + '/' + file_name + '.csv')
        # let's read the first row that we skipped separately and keep it as column names and 
        with open(subfolder + '/' + file) as f:
            header = f.readline().split()
        # let's put the header and units in the dictionary
        data[station][file].columns = header
        print(data[station][file].head())
############### Project notes ################


# TODO: based on my short coversation with Brandon on 2021-07-14, we need to do the following:
# Get the time data from the link shared and convert it into the format you will share (for 2020, 2021, 2022)
# Get the spectral data from 2010 to 2022 (for now). ask Vabhav to give us a sample of spectral data, he needs.
    # if the spectral data from NBDC can be used, then we can use it. Otherwise, we need to generate that data
    # from the time data.