# gnss_interpolate.py
# Description: Interpolate position from POS file for each depth sounding in _sonar file
#
# Author: Tony Furey
# Date: October 12, 2022

# Import Libraries
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime


class GnssInterpolation:

    def interpolate_ers(self, pos_file, sonar_file):
        print('GNSS_Processing: entering gnss_interpolate() function')

        # open files for reading and writing
        if os.path.exists(pos_file):
            pos_file = open(pos_file, 'r')
            gnss_contents = pos_file.readlines()
            pos_file.close()
            print('read .pos file successfully')
            sonar_file = pd.read_csv(sonar_file, delimiter=';')

            # remove .pos header
            header_end_index = self.identify_pos_header(gnss_contents)
            gnss_contents = gnss_contents[header_end_index:]
            print('identified .pos header successfully')

            # separate header from contents and generate dataframe
            header_split = gnss_contents[0].split()
            gnss_contents = gnss_contents[1:]

            gnss_df = []
            for i in range(len(gnss_contents)):
                data = ' '.join(gnss_contents[i].split())
                gnss_df.append(data)

            gnss_contents = pd.DataFrame(gnss_df)
            gnss_contents = gnss_contents[0].str.split(' ', -1, expand=True)
            gnss_contents.columns = header_split

            # interpolate position for depth soundings
            return self.interpolate_pos(gnss_contents, sonar_file)

        else:
            raise IOError('POS file does not exist')

    def identify_pos_header(self, file_contents):
        index = 0
        count = 0
        for line in file_contents:
            if count == 1:
                return index
            elif line[0:5] == 'NOTE:':
                index += 1
                count += 1
            else:
                index += 1

    def interpolate_pos(self, gnss_contents, sonar_contents):
        # Loop to perform time matching and interpolation
        # convert date-time to timestamp
        sonar_contents['Timestamp'] = sonar_contents['Timestamp'].apply(lambda a: datetime.strptime(a, '%Y-%m-%d %H:%M:%S.%f').timestamp())
        gnss_contents['Timestamp'] = gnss_contents['YEAR-MM-DD'] + ' ' + gnss_contents['HR:MN:SS.SS']
        gnss_contents['Timestamp'] = gnss_contents['Timestamp'].apply(lambda a: datetime.strptime(a, '%Y-%m-%d %H:%M:%S.%f').timestamp())

        # initialize lists
        x = []
        y = []
        z = []

        t = 0  # loop counter
        for entry in sonar_contents['Timestamp']:
            ts0 = sonar_contents['Timestamp'].values[t]
            if ts0 > gnss_contents['Timestamp'].max():
                break

            t0 = gnss_contents[gnss_contents['Timestamp'] > ts0].min()  # Does this cause issues if SONAR was not running at start?
            t0 = t0['Timestamp']
            t1 = gnss_contents[gnss_contents['Timestamp'] > t0].min()  # Does this cause issues if SONAR was not running at end?
            t1 = t1['Timestamp']

            x0 = gnss_contents.loc[gnss_contents['Timestamp'] == t0, 'UTM_EASTING'].item()
            x1 = gnss_contents.loc[gnss_contents['Timestamp'] == t1, 'UTM_EASTING'].item()

            y0 = gnss_contents.loc[gnss_contents['Timestamp'] == t0, 'UTM_NORTHING'].item()
            y1 = gnss_contents.loc[gnss_contents['Timestamp'] == t1, 'UTM_NORTHING'].item()

            z0 = gnss_contents.loc[gnss_contents['Timestamp'] == t0, 'H:CGVD2013(m)'].item()
            z1 = gnss_contents.loc[gnss_contents['Timestamp'] == t1, 'H:CGVD2013(m)'].item()

            dt = float(t1) - float(t0)  # ADD CHECK HERE AND FLAG LARGE GAPS
            # checking for gaps in position data greater than 10 seconds
            if dt > 10:
                print("Gap in GNSS position from ", t0, " to ", t1, " seconds.")
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

            if t == len(sonar_contents) or t == len(gnss_contents):  # CHECK ON THIS BREAK
                print('GNSS interpolation completed successfully')
                break

        ers = pd.DataFrame({'Timestamp': sonar_contents['Timestamp'].values[0:len(x)], 'UTM_EASTING': np.array(x), 'UTM_NORTHING'
                           : np.array(y), 'H:CGVD2013(m)': np.array(z), 'Depth': sonar_contents['Depth'].values[0:len(x)]})
        return ers.to_csv('er_soundings.csv', header=True, index=False)


# MAIN

# get pos file path and sonar file path as CLI parameter
if len(sys.argv) != 3:
    sys.stderr.write("Usage: gnss_interpolate.py pos-file-path sonar-file-path\n")
    sys.exit(1)

posFilePath = sys.argv[1]
sonarFilePath = sys.argv[2]

# Create and call GNSS Interpolation

gnss_inter = GnssInterpolation()
gnss_inter.interpolate_ers(posFilePath, sonarFilePath)

# The er_soundings file must match the svp Hycom lookup format in Khalil's code. Check this.
# Add interpolation of IMU data.
