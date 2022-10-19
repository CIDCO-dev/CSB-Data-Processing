# Updated by Tony Furey on 2022-10-19
# Changes made to sort_gps_readings() to qualify as either ERS, WLRS, or INVALID.

import os
import datetime
import sys

class GnssQualification:

    # Returns True/False if GNSS data is valid by examining quality metrics from the PPP pos file
    def validateGnss(self,pos_file):
        print('GNSS_Processing: entering qualify_ppp_output() function')

        # open files for reading and writing
        if os.path.exists(pos_file):
            pos_file = open(pos_file, "r")
            gnss_contents = pos_file.readlines()
            pos_file.close()  # close the file
            print('read .pos file successfully')

            # remove .pos nrcan_header
            header_end_index = self.identify_pos_header(gnss_contents)
            gnss_contents = gnss_contents[header_end_index:]
            print('identified pos header successfully')

            # seperate header from contents
            header = gnss_contents[0]
            header_split = gnss_contents[0].split()
            gnss_contents = gnss_contents[1:]

            # examine and validate GNSS readings
            return self.sort_gps_readings(header_split, gnss_contents)

        else:
            raise IOError("POS file does not exist")

    # helper: identify .pos header
    def identify_pos_header(self, file_contents):
        index = 0
        count = 0
        for line in file_contents:
            if count == 1:
                return index
            elif line[0:5] == "NOTE:":
                index += 1
                count += 1
            else:
                index += 1

    # helper: sort gps reading for gnss or tide v.reference
    def sort_gps_readings(self, header, file_contents):
        print('GNSS_Processing: entering sort_gps_readings() function')

        # threshold variables (used for gps sorting)
        nsv_index = "NSV"
        nsv_ppp = 6
        gdop_index = "GDOP"
        gdop_ppp = 3.5  # increase value more realistic for arctic
        sdlat_index = "SDLAT(95%)"
        sdlat_ppp = 5.0
        sdlon_index = "SDLON(95%)"
        sdlon_ppp = 5.0
        sdhgt_index = "SDHGT(95%)"
        sdhgt_ppp = 0.5
        #sdclk_index = "SDCLK(95%)"
        #sdclk_ppp = 3.0

        # make appropriate indices for each indicator
        nsv_index = header.index(nsv_index)
        gdop_index = header.index(gdop_index)
        sdlat_index = header.index(sdlat_index)
        sdlon_index = header.index(sdlon_index)
        sdhgt_index = header.index(sdhgt_index)
        #sdclk_index = header.index(sdclk_index)

        # sort gps readings
        for line in file_contents:
            lines = line.split()
            nsv_reading = float(lines[nsv_index])
            gdop_reading = float(lines[gdop_index])
            sdlat_reading = float(lines[sdlat_index])
            sdlon_reading = float(lines[sdlon_index])
            sdhgt_reading = float(lines[sdhgt_index])
            #sdclk_reading = float(lines[sdclk_index])

            if nsv_reading > nsv_ppp and gdop_reading < gdop_ppp and sdlat_reading < sdlat_ppp and sdlon_reading < \
                    sdlon_ppp and sdhgt_reading < sdhgt_ppp:
                return print('GNSS data is valid, proceed to ERS')

            elif nsv_reading > nsv_ppp and gdop_reading < gdop_ppp and sdlat_reading < sdlat_ppp and sdlon_reading < \
                    sdlon_ppp and sdhgt_reading > sdhgt_ppp:
                return print('GNSS data acceptable for WLRS')

            else:
                return print('GNSS data is invalid.')


#######################################
# MAIN

# Get pos file path as CLI parameter

if len(sys.argv) != 2:
    sys.stderr.write("Usage: gnss_qualify.py pos-file-path\n")
    sys.exit(1)

posFilePath = sys.argv[1]

# Create and call GNSS qualification

gnss = GnssQualification()
gnss.validateGnss(posFilePath)
