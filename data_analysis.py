import numpy as np
from scipy.io import  loadmat
import matplotlib.pyplot as plt

ROOT_DIR = '/home/masoudmim/Documents/Projects/wave-collaboration-project/data/'
data_2016 = loadmat(ROOT_DIR+'Standard_Met_41046/41046_2016.mat')

# total wave energy calculated for the following stations for 11 years:
# 41043, 41046, 42056, 42057, 42058, 42059, 42060
# using both average wave period (APD), dominant wave period (DPD)
wave_energy_total = loadmat( ROOT_DIR+'WaveEnergyTotal.mat' )

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
station_name_lst = []
years = np.arange(2008, 2019)
for counter, (name, power) in enumerate(wave_energy_total.items()):
    station_name = name.split('_')[1]
    station_name_lst.append(station_name)
    wave_period = name.split('_')[-1].upper()
    # print(station_name, wave_period, power)
    if wave_period == 'APD':
        ax[0].plot(years, power, label=f"{station_name}_{wave_period}", marker="o") 
    elif wave_period == 'DPD':
        ax[1].plot(years, power, label=f"{station_name}_{wave_period}", marker = "o")  

for a in ax:
    a.legend(loc='upper right')
    a.set_title('Total wave energy for 11 years')
    a.set_xlabel('Year')
    a.set_ylabel('Total wave energy')
    a.set_xticks(years)
    a.set_xticklabels(years, rotation=45)
    a.grid(True)

# plt.show()
plt.savefig(ROOT_DIR+'total_wave_energy.png')
