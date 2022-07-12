'''
This module is designed to qualify the GNSS aquisition quality 
in order to access to proceed to apply vertical referencing via
GPS-tides or model-tides approach. 
Uses the GDOP, NSV, STDEV as parameters for qualification. 
Author: Khaleel Arfeen
Email: k.a@unb.ca
Version: 1.1.0
'''

import os 
import datetime
import sys

class GNSS_Processing:

	nrcan_script="csrs_ppp_cgi_browser.py"

	def __init__(self, rnx_file, working_dir):
		self.rnx_file = rnx_file #ie. "C:/PPP/work/16_32_34-2018_08_02-gps.18o"
		self.working_dir = working_dir #ie. "C:/PPP/work/"
		self.nrcan_script = self.nrcan_script
		self.nrcan_username = 'k.a@unb.ca'
		print 'GNSS_Processing: initialized'

	'''
	main: inputs a rinex file and output path 
	runs NRCAN PPP script which will process
	the rinex file and save to the output path
	'''
	def apply_nrcan_ppp(self):
		print 'GNSS_Processing: entering apply_nrcan_ppp() function'

		rnx_file = self.rnx_file
		working_dir = self.working_dir
		
		#check working_dir exists
		output_check = os.path.exists(working_dir)
		
		#check rnx_file exists
		rinex_check = os.path.exists(working_dir + rnx_file)
		
		#check working_dir only contains rinex
		if output_check and rinex_check:
			current_directory_files = os.listdir(working_dir)
		
			#delete all files except for rinex
			if len(current_directory_files) > 1:
				#get rinex extention
				rinex_extention = rnx_file.split(".")[-1]
				for file in current_directory_files:
					if not file.endswith(rinex_extention):
						os.remove(os.path.join(working_dir, file))
	
		#call nrcan PPP script
		if output_check and rinex_check:

			try:
					os.system("python {} --user_name {} --lang en --ref NAD83 --epoch CURR --mode Kinematic --rnx {} --path {}"\
						.format(self.nrcan_script, self.nrcan_username, rnx_file, working_dir))
					print 'GNSS_Processing: exiting apply_nrcan_ppp() function'
					return 0

			except IOError:
					io_error = "IOError: check that file {} or destination {} exists"\
													.format(rnx_file, working_dir) 
					print io_error
					return io_error

			except ConnectionError:
					conn_error = "ConnectionError: Could not connect to NRCAN Server"
					print conn_error
					return conn_error

			except FileNotFoundError:
					file_missing_error = "FileNotFoundError: check that file {} or destination {} exists"\
																		.format(rnx_file, working_dir)
					print file_missing_error
					return file_missing_error

		else:
			return "IOError: check that file {} or destination {} exists"\
										.format(rnx_file, working_dir)

	'''
	main: inputs the name of the position file from the PPP output
	will qualify the gps positions based on GDOP and NSV.
	'''
	def qualify_ppp_output(self):
		print 'GNSS_Processing: entering qualify_ppp_output() function'
		
		pos_file_name = self.rnx_file.split('.')[0] + '.pos'
		working_dir = self.working_dir


		#check pos file exists
		try:
			file_exists = os.path.exists(working_dir + pos_file_name)
		except IOError:
			io_error = "IOError: check that file {} or destination {} exists".format(pos_file_name, working_dir) 
			print io_error
			return io_error

		#open files for reading and writing
		if file_exists:
			pos_file_path = working_dir + pos_file_name
			pos_file = open(pos_file_path,"r")
			gnss_contents = pos_file.readlines()
			pos_file.close() # close the file
			print 'read .pos file successfully'

			sorted_file_path = pos_file_name.split(".")[0] + ".srt"
			gnss_sorted = open(working_dir + sorted_file_path,"w")
			print 'opened .srt file successfully'

			#remove .pos nrcan_header
			header_end_index = self.identify_pos_header(gnss_contents)
			gnss_contents = gnss_contents[header_end_index:]
			print 'identified pos header successfully'

			#seperate header from contents
			header = gnss_contents[0]
			header_split = gnss_contents[0].split()
			gnss_contents = gnss_contents[1:]

			#sort GNSS readings
			gnss_v_ref, tide_v_ref = self.sort_gps_readings(header_split, gnss_contents)

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
			print 'closed pos file successfully'
			print 'GNSS_Processing: exiting qualify_ppp_output() function'
			return 0

		else:
			io_error = "IOError: check that file {} or destination {} exists".format(pos_file_name, working_dir) 
			print io_error
			return io_error

	#helper: identify .pos header
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

	#helper: sort gps reading for gnss or tide v.reference
	def sort_gps_readings(self, header, file_contents):
		print 'GNSS_Processing: entering sort_gps_readings() function'

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
	
		#data to be returned
		for_gnss_v_ref = []
		for_tide_v_ref = []
	
		#make appropriate indices for each indicator
		nsv_index = header.index(nsv_index)	
		gdop_index = header.index(gdop_index)
		sdlat_index = header.index(sdlat_index)
		sdlon_index = header.index(sdlon_index)
		sdhgt_index = header.index(sdhgt_index)
	
		#sort gps readings
		for line in file_contents:
			lines = line.split()
			nsv_reading = float(lines[nsv_index])
			gdop_reading = float(lines[gdop_index])
			sdlat_reading = float(lines[sdlat_index])
			sdlon_reading = float(lines[sdlon_index])
			sdhgt_reading = float(lines[sdhgt_index])
	
			if nsv_reading >= nsv_ppp and gdop_reading <= gdop_ppp and sdlat_reading <= sdlat_ppp \
			and sdlon_reading <= sdlon_ppp and sdhgt_reading <= sdhgt_ppp:
				for_gnss_v_ref.append(line)
			else:
				for_tide_v_ref.append(line)
		
		print 'GNSS_Processing: exiting sort_gps_readings() function'
		return for_gnss_v_ref, for_tide_v_ref

def check_for_args():
	if len(sys.argv) < 3:
		return False
	return True
if __name__ == "__main__":
	if check_for_args():
		gnss = GNSS_Processing(sys.argv[1], sys.argv[2])
		gnss.apply_nrcan_ppp()
		gnss.qualify_ppp_output()
	else:
		print "[+] No arguments provided."
		print "[+]  "
		print "[+] ------- Usages -------"
		print "[+] python gnss_qualification.py 'RINEX_file' 'work_directory'"
		print "[+]  "
		print "[+] And also, for it to work, python need to run this file"
		print "[+] within the directory #CSB_Processing_Scripts/1. GPS_Qualification"
		

gnss = GNSS_Processing("16_32_34-2018_08_02-gps.18o", "C:/PPP/work/")
gnss.apply_nrcan_ppp()
gnss.qualify_ppp_output()