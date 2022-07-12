import os

'''
input:
DIR FRAME        STN         DOY YEAR-MM-DD HR:MN:SS.SSS NSV GDOP    SDC    SDP       DLAT(m)       DLON(m)       DHGT(m)         CLK(ns)   TZD(m)  SLAT(m)  SLON(m)  SHGT(m) SCLK(ns)  STZD(m) LAT(d) LAT(m)    LAT(s) LON(d) LON(m)    LON(s)   HGT(m) CGVD28_HTv2.0_Height NORTHING(m)  EASTING(m) ZONE SCALE_FACTOR HEMI   AM COMBINED_SCALE_FACTOR 
BWD NAD83(CSRS) SITE 265.5796412 2017-09-22 13:54:41.000   9  3.4   1.71 0.0085       174.750       226.064        -5.588         -54.356   2.3791    0.136    0.084    0.166    0.234   0.0049     61      2 47.26018    -69     38 19.34244       -15.305        5.554  6768130.657  465505.887   19      0.99961458 N   3 0.99961698 

output:
lon            lat      year     dayofyear    hours    minutes    seconds
-153.868    58.004000    2014    310           00       00          00
'''

# input a .srt and command and converts to input for tidecor
def srt_to_nav(command, srt_file_name, output_path):

	#### resuse code from gps_qualification.py(qualify_ppp_output)

	#check pos file exists
	file_exists = os.path.exists(output_path+srt_file_name)

	#open files for reading and writing

	#retrieve requested data from .srt and close
	if file_exists:
		srt_file_path = output_path+srt_file_name
		srt_file = open(srt_file_path,"r")		
		srt_contents = srt_file.readlines()

		if command == "tide" or command == "gnss":
			#retrive only data for tides
			srt_contents = identify_srt_header(srt_contents, command)
		# else:
		# 	gnss_contents, tide_contents = identify_srt_header(srt_contents, command)

		srt_file.close() # close the file

		#open .gnav or .tnav file for writing contents
		if command == "tide":
			new_file_name = srt_file_name.split(".")[0] + ".tnav"
		if command == "gnss":
			new_file_name = srt_file_name.split(".")[0] + ".gnav"
		nav_file_path = output_path+new_file_name
		nav_file = open(nav_file_path,"w")

		#write to .nav file
		header = 'lon,lat,year,dayofyear,hours,minutes,seconds\n'
		#nav_file.write(header) #not needed for tidecor input
	
		for line in srt_contents:
			line = line.split()
	
			if len(line) == 0:
				pass
			else:
				nav_formatted = format_as_nav(line)
				nav_formatted = ' '.join(map(str, nav_formatted)) 
				nav_file.write(nav_formatted+"\n")
	
		nav_file.close()
		return 0

	else:
		io_error = "IOError: check check that file {} or destination {} exists".format(srt_file_name, output_path) 
		return io_error

#helper: identify .srt content header positions and returns appropriate data based on command
def identify_srt_header(file_contents, command):

	#.srt possible headers
	tide = "#FOR TIDAL VERTICAL REFERENCING:"
	gnss = "#FOR GNSS VERTICAL REFERENCING:"

	#track index 
	tide_index = 0
	gnss_index = 0

	index = 0
	for line in file_contents:
		index+=1
		if line[:1] == "#":
			if tide in line:
				tide_index = index
			if gnss in line:
				gnss_index = index
		else:
			pass

	if command == "tide":
		return file_contents[tide_index:index]
	if command == "gnss":
		return file_contents[gnss_index:tide_index-2]
	# else:
	# 	return file_contents[gnss_index:tide_index-2], file_contents[tide_index:index]
#document: .srt file constaints (affects how this will sort)
#might be better to avoid this altogether and convert entire file to .nav
#think about including no command option

#helper: sort reading into nav format
#note: index used are based on nrcan ppp output 
def format_as_nav(reading):
	lat = convert_dms_to_dd(float(reading[20]), float(reading[21]), float(reading[22]))
	lon = convert_dms_to_dd(float(reading[23]), float(reading[24]), float(reading[25]))
	year = int(reading[4].split('-')[0])
	dayofyear = int(float(reading[3]))
	time = reading[5].split(':')
	hours = int(time[0])
	minutes = int(time[1])
	seconds = float(time[2])
	return [lon, lat, year, dayofyear, hours, minutes, seconds]

#helper: converts decimal,minute,seconds to decimal degrees
def convert_dms_to_dd(dec, min, sec):
	if dec < 0:
		min = float(min) / 60
		sec = float(sec) / 3600
		return round(dec-min-sec, 4)
	else:
		min = float(min) / 60
		sec = float(sec) / 3600
		return round(dec+min+sec, 4)


srt_to_nav('tide', "15_17_52-2018_05_22-gps.srt", "C:/PPP/")
srt_to_nav('gnss', "15_17_52-2018_05_22-gps.srt", "C:/PPP/")