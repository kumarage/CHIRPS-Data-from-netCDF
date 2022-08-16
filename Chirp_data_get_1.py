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

fn1 = 'chirps-v2.0.1982.days_p25.nc'

dat = Dataset(fn1)
time_p = dat.variables['time']
lat_p = dat.variables['latitude']
lon_p = dat.variables['longitude'] 

i_lon_left  = find_nearest(lon_p,lon_min_lk)-1
i_lon_right = find_nearest(lon_p,lon_max_lk)
i_lat_down  = find_nearest(lat_p,lat_min_lk)
i_lat_up 	= find_nearest(lat_p,lat_max_lk)
#print(i_lon_left,i_lon_right)
#print(i_lat_down,i_lat_up)

lat_span = i_lat_up - i_lat_down+1
lon_span = i_lon_right - i_lon_left+1
#pre = np.zeros((365,lat_span,lon_span))

print(lat_span,lon_span)

mis_lat = []
mis_lon = []

for i in range(0,365):
	tot_pre=0.0
	for j in range(0,lat_span):
		for k in range(0,lon_span):
			jj = i_lat_down+j
			kk = i_lon_left+k
			val = dat.variables['precip'][i,jj,kk]
			if val>=0.0:
				tot_pre = tot_pre + val
				if i==0:
					mis_lat.append(jj)
					mis_lon.append(kk)

nn = len(mis_lon)
print(nn)
pre = np.zeros((365,nn))
points = np.zeros((2,nn))
for i in range(0,nn):
	points[0][i] = dat.variables['latitude'][mis_lat[i]]
	points[1][i] = dat.variables['longitude'][mis_lon[i]]
	for j in range(0,365):
		pre[j][i] = dat.variables['precip'][j,mis_lat[i],mis_lon[i]]


#print(pre[0][:])
dates = []
sdate = date(1982,1,1)
edate = date(1982,12,31)

delta = edate - sdate

for d in range(delta.days+1):
	day = sdate + timedelta(days=d)
	dates.append(day.strftime('%m/%d/%Y'))	

ndf = pd.DataFrame({'Date': dates})
ndf.to_excel('1982_Precip.xlsx')

np.savetxt("precips_1982.csv", pre, delimiter=",")
np.savetxt("points.csv", points, delimiter=",")
#coord = pd.DataFrame({'Latitude':mis_lat, 'longitude':mis_lon})
#coord.to_csv('coords.csv')
#
#
#.................................Getting Data......................................