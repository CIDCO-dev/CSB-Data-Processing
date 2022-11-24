"""
gnss_interpolate.py
Description: Interpolate position from POS file for each depth sounding in _sonar file

Author: Tony Furey
Date: October 12, 2022

Updates:
1. TF - Oct 19, 2022: Added timestamp sorting and fixed handling of missing data at beginning/end of files.
2. TF - Oct 20, 2022: Added gap checks and IMU data handling.
3. TF - Oct 27, 2022: Fixed heading interpolation and added conversion from dms to dd for latitude and longitude.
"""

# Import Libraries
import pandas as pd
import numpy as np
import os
import sys
import math
from datetime import datetime


class GnssInterpolation:

    def interpolate_ers(self, pos_file, sonar_file, imu_file):
        print('GNSS_Processing: entering gnss_interpolate() function')

        # open files for reading and writing
        if os.path.exists(pos_file):
            pos_file = open(pos_file, 'r')
            gnss_contents = pos_file.readlines()
            pos_file.close()
            print('read .pos file successfully')
            sonar_file = pd.read_csv(sonar_file, delimiter=';')
            print('read sonar file successfully')
            imu_file = pd.read_csv(imu_file, delimiter=';')
            print('read imu file successfully')

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
            return self.interpolate_pos(gnss_contents, sonar_file, imu_file)

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

    def interpolate_pos(self, gnss_contents, sonar_contents, imu_contents):
        # Loop to perform time matching and interpolation
        # convert date-time to timestamp
        gnss_contents['Timestamp'] = gnss_contents['YEAR-MM-DD'] + ' ' + gnss_contents['HR:MN:SS.SS']
        gnss_contents['Timestamp'] = gnss_contents['Timestamp'].apply(lambda a: datetime.strptime(a, '%Y-%m-%d %H:%M:%S.%f').timestamp())
        sonar_contents['Timestamp'] = sonar_contents['Timestamp'].apply(lambda a: datetime.strptime(a, '%Y-%m-%d %H:%M:%S.%f').timestamp())
        imu_contents['Timestamp'] = imu_contents['Timestamp'].apply(lambda a: datetime.strptime(a, '%Y-%m-%d %H:%M:%S.%f').timestamp())

        # sort data by timestamp
        gnss_contents = gnss_contents.sort_values('Timestamp')
        sonar_contents = sonar_contents.sort_values('Timestamp')
        imu_contents = imu_contents.sort_values('Timestamp')

        # convert lat & lon DMS to DD
        lat_list = []
        lon_list = []

        counter = 0
        for row in range(len(gnss_contents)):
            lat_dd = float(gnss_contents['LATDD'].values[counter]) + (float(gnss_contents['LATMN'].values[counter]) / 60) + (float(gnss_contents['LATSS'].values[counter]) / 3600)
            lon_dd = float(gnss_contents['LONDD'].values[counter]) + (float(gnss_contents['LONMN'].values[counter]) / 60) + (float(gnss_contents['LONSS'].values[counter]) / 3600)
            lat_list.append(lat_dd)
            lon_list.append(lon_dd)
            counter += 1

        gnss_contents['latitude'] = np.array(lat_list)
        gnss_contents['longitude'] = np.array(lon_list)

        # initialize lists
        x = []  # latitude
        y = []  # longitude
        z = []  # ellipsoidal height
        h = []  # heading
        p = []  # pitch
        r = []  # roll
        s = []  # sounding
        timestamps = []

        t = 0  # loop counter
        for row in range(len(sonar_contents)):
            ts0 = sonar_contents['Timestamp'].values[t]

            while ts0 < gnss_contents['Timestamp'].min() or ts0 < imu_contents['Timestamp'].min():
                t += 1
                ts0 = sonar_contents['Timestamp'].values[t]

            if ts0 > [gnss_contents['Timestamp'].max() or imu_contents['Timestamp'].max()]:
                break

            # find timestamp in position and attitude data before and after the current sounding
            # position
            tp0 = gnss_contents[gnss_contents['Timestamp'] < ts0].max()
            tp0 = tp0['Timestamp']
            tp1 = gnss_contents[gnss_contents['Timestamp'] > ts0].min()
            tp1 = tp1['Timestamp']
            # attitude
            ta0 = imu_contents[imu_contents['Timestamp'] < ts0].max()
            ta0 = ta0['Timestamp']
            ta1 = imu_contents[imu_contents['Timestamp'] > ts0].min()
            ta1 = ta1['Timestamp']

            # latitude ## NEED TO CONVERT DEG - MM - SS.SSSSS to Decimal Degrees ##
            x0 = gnss_contents.loc[gnss_contents['Timestamp'] == tp0, 'longitude'].item()
            x1 = gnss_contents.loc[gnss_contents['Timestamp'] == tp1, 'longitude'].item()

            # longitude ## NEED TO CONVERT DEG - MM - SS.SSSSS to Decimal Degrees ##
            y0 = gnss_contents.loc[gnss_contents['Timestamp'] == tp0, 'latitude'].item()
            y1 = gnss_contents.loc[gnss_contents['Timestamp'] == tp1, 'latitude'].item()

            # height
            z0 = gnss_contents.loc[gnss_contents['Timestamp'] == tp0, 'HGT(m)'].item()
            z1 = gnss_contents.loc[gnss_contents['Timestamp'] == tp1, 'HGT(m)'].item()

            # heading
            h0 = float(imu_contents.loc[imu_contents['Timestamp'] == ta0, 'Heading'].item())
            h1 = float(imu_contents.loc[imu_contents['Timestamp'] == ta1, 'Heading'].item())

            # pitch
            p0 = float(imu_contents.loc[imu_contents['Timestamp'] == ta0, 'Pitch'].item())
            p1 = float(imu_contents.loc[imu_contents['Timestamp'] == ta1, 'Pitch'].item())

            # roll
            r0 = float(imu_contents.loc[imu_contents['Timestamp'] == ta0, 'Roll'].item())
            r1 = float(imu_contents.loc[imu_contents['Timestamp'] == ta1, 'Roll'].item())

            # check for gaps in position and attitude data
            dtp = float(tp1) - float(tp0)
            dta = float(ta1) - float(ta0)

            # checking for gaps in position data greater than 2 seconds
            if dtp > 2:
                print("Gap in GNSS data from ", tp0, " to ", tp1, " seconds.")

            # checking for gaps in position data greater than 2 seconds
            if dta > 2:
                print("Gap in attitude data from ", ta0, " to ", ta1, " seconds.")

            dt_ps = float(ts0) - float(tp0)
            dt_as = float(ts0) - float(ta0)

            dx = float(x1) - float(x0)
            dy = float(y1) - float(y0)
            dz = float(z1) - float(z0)
            #dh = float(h1) - float(h0)
            dp = float(p1) - float(p0)
            dr = float(r1) - float(r0)

            xs0 = float(x0) + (dx * (dt_ps / dtp))
            ys0 = float(y0) + (dy * (dt_ps / dtp))
            zs0 = float(z0) + (dz * (dt_ps / dtp))

            # check if heading oscillates about 0 deg
            if 350 <= h0 <= 360 and 0 <= h1 <= 10:
                h1 = h1 + 360
                #return h1
            if 0 <= h0 <= 10 and 350 <= h1 <= 360:
                h0 = h0 + 360
                #return h0

            dh = float(h1) - float(h0)
            hs0 = float(h0) + (dh * (dt_as / dta))

            if hs0 > 360:
                hs0 = hs0 - 360
                #return hs0

            ps0 = float(p0) + (dp * (dt_as / dta))
            rs0 = float(r0) + (dr * (dt_as / dta))
            s0 = sonar_contents.loc[sonar_contents['Timestamp'] == ts0, 'Depth'].item()

            x.append(xs0)
            y.append(ys0)
            z.append(zs0)
            h.append(hs0)
            p.append(ps0)
            r.append(rs0)
            s.append(s0)
            timestamps.append(ts0)

            t += 1

            if t == len(sonar_contents) or t == len(gnss_contents) or t == len(imu_contents):
                print('GNSS and IMU interpolation completed successfully')
                break

        # convert depth to travelTime (one-way)
        ss = 1490  # set the sound speed used during data collection (m/s)
        tt_list = []
        for depth in range(len(s)):
            tt = s[depth] / (2 * ss)
            tt_list.append(tt)

        # convert timestamps back to datetime
        dt_list = []
        for timestamp in range(len(timestamps)):
            dt = datetime.fromtimestamp(timestamps[timestamp])
            dt_list.append(dt)

        # convert degrees to radians (not required for input to batch mode processing)
        #y = np.deg2rad(y)
        #x = np.deg2rad(x)
        #h = np.deg2rad(h)
        #p = np.deg2rad(p)
        #r = np.deg2rad(r)

        # compile dataframes
        ers = pd.DataFrame({'travelTime': np.array(tt_list), 'latitude': np.array(y), 'longitude': np.array(x),
                            'height': np.array(z), 'heading': np.array(h), 'pitch': np.array(p),
                            'roll': np.array(r), 'depth': np.array(s), 'datetime': np.array(dt_list)})
        georef_batch_input = pd.DataFrame({'travelTime': np.array(tt_list), 'latitude': np.array(y), 'longitude': np.array(x),
                            'height': np.array(z), 'heading': np.array(h), 'pitch': np.array(p),
                            'roll': np.array(r)})

        return georef_batch_input.to_csv('georef_batch_input.txt', sep=' ', header=False, index=False)


#
# MAIN

# get pos file path and sonar file path as CLI parameter
if len(sys.argv) != 4:
    sys.stderr.write("Usage: gnss_interpolate.py pos-file-path sonar-file-path imu-file-path\n")
    sys.exit(1)

posFilePath = sys.argv[1]
sonarFilePath = sys.argv[2]
imuFilePath = sys.argv[3]

# Create and call GNSS Interpolation

gnss_inter = GnssInterpolation()
gnss_inter.interpolate_ers(posFilePath, sonarFilePath, imuFilePath)

# line for testing script:
# gnss_inter.interpolate_ers('20220602_005419.pos', '20220602_005430_sonar.txt', '20220602_005430_imu.txt')
