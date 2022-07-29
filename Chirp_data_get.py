import netCDF4 as nc
import numpy as np
#import datetime as dt
from datetime import date, timedelta
import pandas as pd
import re
from matplotlib import pyplot as plt
from netCDF4 import Dataset, date2index, num2date, date2num
import xarray
#support website: https://www.pythontutorial.net/tkinter/tkinter-entry/
#datetime: https://www.code4example.com/python/python-user-input-date-and-time/

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

#Sri Lanka enclosure box
lat_min_lk = 5.9320
lat_max_lk = 9.7938
lon_min_lk = 79.8612
lon_max_lk = 81.8659

fn1 = 'chirps-v2.0.2021.days_p25.nc'

dat = Dataset(fn1)
time_p = dat.variables['time']
lat_p = dat.variables['latitude']
lon_p = dat.variables['longitude'] 

i_lon_left  = find_nearest(lon_p,lon_min_lk)-1
i_lon_right = find_nearest(lon_p,lon_max_lk)
i_lat_down  = find_nearest(lat_p,lat_min_lk)
i_lat_up 	= find_nearest(lat_p,lat_max_lk)
print(i_lon_left,i_lon_right)
print(i_lat_down,i_lat_up)

lat_span = i_lat_up - i_lat_down+1
lon_span = i_lon_right - i_lon_left+1
#pre = np.zeros((365,lat_span,lon_span))
pre = np.zeros(365)
print(lat_span,lon_span)

for i in range(0,365):
	tot_pre=0.0
	for j in range(0,lat_span):
		for k in range(0,lon_span):
			jj = i_lat_down+j
			kk = i_lon_left+k
			val = dat.variables['precip'][i,jj,kk]
			if val>0.0:
				tot_pre = tot_pre + val
	pre[i] = tot_pre/(lat_span*lon_span)

#print(pre)
dates = []

sdate = date(2021,1,1)
edate = date(2021,12,31)

delta = edate - sdate

for d in range(delta.days+1):
	day = sdate + timedelta(days=d)
	dates.append(day.strftime('%m/%d/%Y'))

ndf = pd.DataFrame({'Date': dates, 'Precipitation': pre})
ndf.to_excel('2021_Precip.xlsx')

#.................................Getting Data.................................................