# POSmatch.py
# Description: Interpolate position from _gnss file for each depth sounding in _sonar file
#
# Author: Tony Furey
# Date: May 9, 2022

# Import Libraries
import pandas as pd
import numpy as np
import os
import re

from datetime import datetime

# Import Data
mylines = []
with open('20220602_005419.srt', 'rt') as myfile:
    for myline in myfile:
        mylines.append(myline.rstrip('\n'))

header = mylines[3].split(' ')
header[:] = [x for x in header if x.strip()]

substr = '#FOR GNSS VERTICAL REFERENCING:'
count = 0
for line in mylines:
    index = line.find(substr)
    count += 1
    if index == 0:
        print(count)
        break

substr2 = '#FOR TIDAL VERTICAL REFERENCING:'
count2 = 0
for line in mylines:
    index = line.find(substr2)
    count2 += 1
    if index == 0:
        print(count2)
        break

noHeader = mylines[count:count2-3]
parsed = []
for line in noHeader:
    parsed.append(line.split(' '))

for line in parsed:
    line[:] = [x for x in line if x.strip()]

df_ERS = pd.DataFrame(parsed, columns=header)

#pattern = r'\w+.\w+.\w+_\w+_sonar.txt'  # Filename pattern for _sonar files

#for i in os.listdir("C:\\Users\\afurey1\\Downloads\\data"):
#    if re.search(pattern, i):
#        df = pd.read_csv(path + i, delimiter=';', header=0)
#        li_sonar.append(df)

depths = pd.read_csv('20220602_005430_sonar.txt', delimiter=';')

print(df_ERS.head())  # GNSS position data
print(depths.head())  # Sonar data

# Loop to perform time matching and interpolation
# FIX THIS: For Sonar depths outside the observations of position, use velocities to predict position? Or closest
# position in time? Or eliminate?

depths['Timestamp'] = depths['Timestamp'].apply(lambda a: datetime.strptime(a, '%Y-%m-%d %H:%M:%S.%f').timestamp())
df_ERS['Timestamp'] = df_ERS['YEAR-MM-DD'] + ' ' + df_ERS['HR:MN:SS.SS']
df_ERS['Timestamp'] = df_ERS['Timestamp'].apply(lambda a: datetime.strptime(a, '%Y-%m-%d %H:%M:%S.%f').timestamp())

# Initialize lists
x = []
y = []
z = []

t = 0  # Loop counter
for entry in depths['Timestamp']:
    ts0 = depths['Timestamp'].values[t]
    if ts0 > df_ERS['Timestamp'].max():
        break

    t0 = df_ERS[df_ERS['Timestamp'] > ts0].min()  # Does this cause issues if SONAR was not running at start?
    t0 = t0['Timestamp']
    t1 = df_ERS[df_ERS['Timestamp'] > t0].min()  # Does this cause issues if SONAR was not running at end?
    t1 = t1['Timestamp']

    x0 = df_ERS.loc[df_ERS['Timestamp'] == t0, 'UTM_EASTING'].item()
    x1 = df_ERS.loc[df_ERS['Timestamp'] == t1, 'UTM_EASTING'].item()

    y0 = df_ERS.loc[df_ERS['Timestamp'] == t0, 'UTM_NORTHING'].item()
    y1 = df_ERS.loc[df_ERS['Timestamp'] == t1, 'UTM_NORTHING'].item()

    z0 = df_ERS.loc[df_ERS['Timestamp'] == t0, 'H:CGVD2013(m)'].item()
    z1 = df_ERS.loc[df_ERS['Timestamp'] == t1, 'H:CGVD2013(m)'].item()

    dt = float(t1) - float(t0)  # ADD CHECK HERE AND FLAG LARGE GAPS
    dt_ps = float(ts0) - float(t0)

    dx = float(x1) - float(x0)
    dy = float(y1) - float(y0)
    dz = float(z1) - float(z0)

    xs0 = float(x0) + (dx * (dt_ps / dt))
    ys0 = float(y0) + (dy * (dt_ps / dt))
    zs0 = float(z0) + (dz * (dt_ps / dt))

    x.append(xs0)
    y.append(ys0)
    z.append(zs0)

    t += 1

    if t == len(depths) or t == len(df_ERS):  # CHECK ON THIS BREAK
        break

mergedData = pd.DataFrame({'Timestamp': depths['Timestamp'].values[0:len(x)], 'UTM_EASTING': np.array(x), 'UTM_NORTHING'
                          : np.array(y), 'H:CGVD2013(m)': np.array(z), 'Depth': depths['Depth'].values[0:len(x)]})

print(mergedData.head())
print('HOORAY IT WORKED!')
mergedData.to_csv('mergedData.csv', header=True, index=False)
# The mergedData file must match the svp Hycom lookup format in Khalil's code!
# Newest link to look-up table: http://tds.hycom.org/thredds/catalogs/GLBy0.08/expt_93.0.html
