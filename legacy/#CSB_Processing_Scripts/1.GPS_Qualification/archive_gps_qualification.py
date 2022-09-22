'''
This module is designed to qualify the GNSS aquisition quality 
in order to access to proceed to apply vertical referencing via
GPS-tides or model-tides approach. 

Uses the GDOP and NSV as parameters for qualification. 

Author: Khaleel Arfeen
Email: k.a@unb.ca
Version: 1.0.0
'''

import os 
import datetime

'''
inputs a rinex file and output path 
runs NRCAN PPP script which will process
the rinex file and save to the output path
note rnx_file should be entered as a path
'''
def apply_nrcan_ppp(rnx_file, output_path, nrcan_script="csrs_ppp_cgi_browser.py"):

	#default parameters
	#nrcan_script = "csrs_ppp_cgi_browser.py"
	user_name = 'k.a@unb.ca'

	#check output_path exists
	output_check = os.path.exists(output_path)
	#check rnx_file exists
	rinex_check = os.path.exists(rnx_file)
	#check output_path only contains rinex
	if output_check and rinex_check:
		current_directory_files = os.listdir(output_path)
	
		#delete all files except for rinex
		if len(current_directory_files) > 1:
			#get rinex extention
			rinex_extention = rnx_file.split(".")[-1]
			for file in current_directory_files:
				if not file.endswith(rinex_extention):
					os.remove(os.path.join(output_path, file))

	#call nrcan PPP script
	if output_check and rinex_check:
		try:
				os.system("python {} --user_name {} --lang en --ref NAD83 --epoch CURR --mode Kinematic --rnx {} --path {}"\
					.format(nrcan_script, user_name, rnx_file, output_path))
				return 0
		except IOError:
				io_error = "IOError: check check that file {} or destination {} exists".format(rnx_file, output_path) 
				print io_error
				return io_error
		except ConnectionError:
				conn_error = "ConnectionError: Could not connect to NRCAN Server"
				print conn_error
				return conn_error
		except FileNotFoundError:
				file_missing_error = "FileNotFoundError: check check that file {} or destination {} exists".format(rnx_file, output_path)
				print file_missing_error
				return file_missing_error
	else:
		return "IOError: check check that file {} or destination {} exists".format(rnx_file, output_path)

	#call the nrcan script from ..External.csrs_ppp_cgi_browser (X)
	#pass the file name to run (X)
	#pass or default running parameters (X)
	#save to appropriate location (X)
	#make sure output directory is empty (x)
	#flag for corrupt files/not processed (return 1/0 + error)
	#update the metadata (main may do this)
	#add error handling (x)
	#add tests

'''
main: inputs the name of the position file from the PPP output
will qualify the gps positions based on GDOP and NSV.
'''
def qualify_ppp_output(pos_file_name, output_path):
	
	#check pos file exists
	try:
		file_exists = os.path.exists(output_path+pos_file_name)
	except IOError:
		io_error = "IOError: check check that file {} or destination {} exists".format(pos_file_name, output_path) 
		print io_error
		return io_error

	#open files for reading and writing
	if file_exists:
		pos_file_path = output_path+pos_file_name
		pos_file = open(pos_file_path,"r")
		gnss_contents = pos_file.readlines()
		pos_file.close() # close the file

		new_file_name = pos_file_name.split(".")[0] + ".srt"
		sorted_file_path = output_path+new_file_name
		gnss_sorted = open(sorted_file_path,"w")

		#remove .pos nrcan_header
		header_end_index = identify_pos_header(gnss_contents)
		gnss_contents = gnss_contents[header_end_index:]

		#seperate header from contents
		header = gnss_contents[0]
		header_split = gnss_contents[0].split()
		gnss_contents = gnss_contents[1:]

		#sort GNSS readings
		gnss_v_ref, tide_v_ref = sort_gps_readings(header_split, gnss_contents)

		#write to .srt file
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
		return 0

	else:
		io_error = "IOError: check check that file {} or destination {} exists".format(pos_file_name, output_path) 
		print io_error
		return io_error

#helper: sort gps reading for gnss or tide v.reference
def sort_gps_readings(header, file_contents):
	#threshold variables (used for gps sorting)
	nsv_index = "NSV"
	nsv_ppp = 6
	gdop_index = "GDOP"
	gdop_ppp = 3.5 #increase value more realistic for arctic
	sdlat_index = "SDLAT(95%)"
	sdlat_ppp = 5.0
	sdlon_index = "SDLON(95%)"
	sdlon_ppp = 5.0
	sdhgt_index = "SDHGT(95%)"
	sdhgt_ppp = 0.5
	sdclk_index = "SDCLK(95%)"
	sdclk_ppp = 3.0

	#data to be returned
	for_gnss_v_ref = []
	for_tide_v_ref = []

	#make appropriate indices for each indicator
	nsv_index = header.index(nsv_index)	
	gdop_index = header.index(gdop_index)
	sdlat_index = header.index(sdlat_index)
	sdlon_index = header.index(sdlon_index)
	sdhgt_index = header.index(sdhgt_index)
	sdclk_index = header.index(sdclk_index)

	#sort gps readings
	for line in file_contents:
		lines = line.split()
		nsv_reading = float(lines[nsv_index])
		gdop_reading = float(lines[gdop_index])
		sdlat_reading = float(lines[sdlat_index])
		sdlon_reading = float(lines[sdlon_index])
		sdhgt_reading = float(lines[sdhgt_index])
		sdclk_reading = float(lines[sdclk_index])

		if nsv_reading >= nsv_ppp and gdop_reading <= gdop_ppp and sdlat_reading <= sdlat_ppp \
		and sdlon_reading <= sdlon_ppp and sdhgt_reading <= sdhgt_ppp and sdclk_reading <= sdclk_ppp:
			for_gnss_v_ref.append(line)
		else:
			for_tide_v_ref.append(line)

	return for_gnss_v_ref, for_tide_v_ref

#helper: identify .pos header
def identify_pos_header(file_contents):
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

	#opens the .pos file and creates two/three lists (x)
	#one list for readings with good GDOP and NSV (gps-tides) (x)
	#one list for readings with bad GDOP and NSV (model-tides) (x)
	#one list for rejected and outlier readings (not implemented)
	#iterates through entire file and sorts based on threshold values (x)
	#flag when complete (return 1/0 + error) (x)
	#update the metadata (main may do this)
	#add proper try-except clause and returns (0/1)
	
apply_nrcan_ppp("C:/PPP/work/16_32_34-2018_08_02-gps.18o", "C:/PPP/work/")
qualify_ppp_output('16_32_34-2018_08_02-gps.pos','C:/PPP/work/')

#apply_nrcan_ppp("D:/Dropbox/Running/ProjectResearch/#Software/Sample_Data_CSB/HydroBall_GjoaHaven/data/GPS/2018_08_02/rinex_RTKLIB/test_srt/HydroBall_20180802.obs", "D:/Dropbox/Running/ProjectResearch/#Software/Sample_Data_CSB/HydroBall_GjoaHaven/data/GPS/2018_08_02/rinex_RTKLIB/test_srt/")
#qualify_ppp_output('HydroBall_20180802.pos','D:/Dropbox/Running/ProjectResearch/#Software/Sample_Data_CSB/HydroBall_GjoaHaven/data/GPS/2018_08_02/Hemisphere.RTKLIB_Compare/RTKLIB/')
												  												
