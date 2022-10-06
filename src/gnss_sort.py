import os
import datetime


class GNSS_Processing:
    nrcan_script = "csrs_ppp_auto.py"

    def __init__(self, pos_file, working_dir):
        self.rnx_file = pos_file  # ie. "20220602_005419.pos"
        self.working_dir = working_dir  # ie. "D:/PyCharmProjects/MASS/"
        self.nrcan_script = self.nrcan_script
        self.nrcan_username = 'afurey1@unb.ca'
        print('GNSS_Processing: initialized')

    def qualify_ppp_output(self):
        print('GNSS_Processing: entering qualify_ppp_output() function')

        pos_file_name = self.rnx_file
        working_dir = self.working_dir

        # check pos file exists
        try:
            file_exists = os.path.exists(working_dir + pos_file_name)
        except IOError:
            io_error = "IOError: check that file {} or destination {} exists".format(pos_file_name, working_dir)
            print(io_error)
            return io_error

        # open files for reading and writing
        if file_exists:
            pos_file_path = working_dir + pos_file_name
            pos_file = open(pos_file_path, "r")
            gnss_contents = pos_file.readlines()
            pos_file.close()  # close the file
            print('read .pos file successfully')

            sorted_file_path = pos_file_name.split(".")[0] + ".srt"
            gnss_sorted = open(working_dir + sorted_file_path, "w")
            print('opened .srt file successfully')

            # remove .pos nrcan_header
            header_end_index = self.identify_pos_header(gnss_contents)
            gnss_contents = gnss_contents[header_end_index:]
            print('identified pos header successfully')

            # seperate header from contents
            header = gnss_contents[0]
            header_split = gnss_contents[0].split()
            gnss_contents = gnss_contents[1:]

            # sort GNSS readings
            gnss_v_ref, tide_v_ref = self.sort_gps_readings(header_split, gnss_contents)

            # write to .srt file
            gnss_sorted.write("GNSS OBSERVATION SORTED - {} \n".format(datetime.datetime.now()))
            gnss_sorted.write("GNSS-Vertical Records {}, GSS-Tidal Records {}".format(len(gnss_v_ref), len(tide_v_ref)))
            gnss_sorted.write("FOR REJECTED READINGS SEE {}.SUM FILE \n\n".format(pos_file_name.split(".")[0]))
            gnss_sorted.write(header + "\n")

            gnss_sorted.write("#FOR GNSS VERTICAL REFERENCING: \n")
            for line in gnss_v_ref:
                gnss_sorted.write(str(line))
            gnss_sorted.write("\n")

            gnss_sorted.write("#FOR TIDAL VERTICAL REFERENCING:\n")
            for line in tide_v_ref:
                gnss_sorted.write(str(line))

            gnss_sorted.close()
            print('closed pos file successfully')
            print('GNSS_Processing: exiting qualify_ppp_output() function')
            return 0

        else:
            io_error = "IOError: check that file {} or destination {} exists".format(pos_file_name, working_dir)
            print(io_error)
            return io_error

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

        # data to be returned
        for_gnss_v_ref = []
        for_tide_v_ref = []

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

            if nsv_reading >= nsv_ppp and gdop_reading <= gdop_ppp and sdlat_reading <= sdlat_ppp \
                    and sdlon_reading <= sdlon_ppp and sdhgt_reading <= sdhgt_ppp:
                for_gnss_v_ref.append(line)
            else:
                for_tide_v_ref.append(line)

        print('GNSS_Processing: exiting sort_gps_readings() function')
        return for_gnss_v_ref, for_tide_v_ref


gnss = GNSS_Processing("20220602_005419.pos", "D:/PyCharmProjects/MASS/")
gnss.qualify_ppp_output()
