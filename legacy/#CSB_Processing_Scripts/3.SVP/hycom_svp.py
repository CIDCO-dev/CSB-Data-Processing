from pydap.client import open_url
from datetime import datetime
import copy
import os
import gsw #gsw==3.0.6
import sys
'''
This module is designed to take the .srt file created from the GNSS processing module and
parse the data to obtain necessary inputs (date, time, latitude, longitude) to the Hycom
Oceanographic model. The script will take this information for each line in the .srt file,
convert it to a Hycom index, query the model, convert the results from hycom indices, create
the sound velocity from model temperatures and salinity and finally save the results as a 
Caris SVP format file.

The script will minimize queries to the Hycom model by keeping a cache of queries and if 
the query is not successful will perform a radial search for the nearest node. 

The model uses the Hycom model to query Temperature-depth and Salinity-depth arrays for
a given location and time. These arrays are then converted to sound velocities using the
TEOS-10 algorithm. 

Author: Khaleel Arfeen
Email: k.a@unb.ca
Version: 1.0.0
'''

class Hycom_SVP_Query:

	gbl_hycom = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_93.0'
	
	def __init__(self, srt_file_name, output_path):
		self.srt_file_name = srt_file_name
		self.output_path = output_path
		self.hycom_url = self.gbl_hycom
		self.srt_contents = False
		self.index = {'header': 0, 'gnss': 0, 'tide': 0}	
		self.header_variables = ''
		self.header_index = {'doy_index': 'DAYofYEAR', 'date_index': 'YEAR-MM-DD', 'time_index': 'HR:MN:SS.SS',\
							'latdd_index': 'LATDD', 'latmn_index': 'LATMN', 'latss_index': 'LATSS',\
							 'londd_index': 'LONDD', 'lonmn_index': 'LONMN', 'lonss_index': 'LONSS'}
		self.srt_line_map_values = {'date_reading': 'date_index', 'time_reading': 'time_index',  'latdd_reading': 'latdd_index',\
						'latmn_reading': 'latmn_index', 'latss_reading': 'latss_index', 'londd_reading': 'londd_index',\
						'lonmn_reading': 'lonmn_index', 'lonss_reading': 'lonss_index'}
		self.srt_line_data = {'date_reading': 0, 'time_reading': 0,  'latdd_reading': 0,\
						'latmn_reading': 0, 'latss_reading': 0, 'londd_reading': 0,\
						'lonmn_reading': 0, 'lonss_reading': 0}
		self.rinex_iterator_retry_attempts = 20
		self.rinex_iterator_retry_count = 0
		self.hycom_epoch = datetime(2000, 01, 01, 00, 00, 00)
		self.hycom_date_zero = 157812
		self.hycom_query_cache = []
		self.hycom_query_flag = []
		self.hycom_db_handle = ''
		self.raw_latdd_londd = []
		self.hycom_salinity_data = []
		self.hycom_temperature_data = []
		self.hycom_depth_array = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 125.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0, 1250.0, 1500.0, 2000.0, 2500.0, 3000.0, 4000.0, 5000.0]
		self.successful_query_srt_index = []

	#open srt file, load contents to memory
	def load_srt_contents(self):
		try:
			file_exists = os.path.exists(self.output_path + self.srt_file_name)
		except IOError:
			io_error = "IOError: check check that file {} or destination {} exists".format(self.srt_file_name, self.output_path) 
			print io_error
			return io_error

		if file_exists:
			srt_file_path = self.output_path + self.srt_file_name
			srt_file = open(srt_file_path,"r")
			self.srt_contents = srt_file.readlines()
			srt_file.close() # close the file

	#helper: identify .pos header locations and assign header variables
	# command: header, gnss, tide indices (self.index)
	def identify_srt_header(self):
		for command in self.index.keys():

			#select identifier for command
			if command == 'header':
				splice = 'DIR FR'
			elif command == 'gnss':
				splice = '#FOR G'
			else:
				splice = '#FOR T'

			#locate command index
			index_value = 0
			flag = 0
			
			for line in self.srt_contents:
				if flag == 1:
					self.index[command] = index_value
				elif line[0:6] == splice:
					flag += 1
				else:
					index_value += 1
		
		self.header_variables = self.srt_contents[self.index['header']]
		self.header_variables = self.header_variables.split()

	#helper: identify index values for required header variables
	#required: time, date, latitude, longitude (self.header_index)
	def identify_header_variables(self):
		for k,v in self.header_index.items():
			self.header_index[k] = self.header_variables.index(v)

	#main: iterate through srt_contents to formulate hycom index values 
	#and facilitate hycom model query and save of svp file
	def rinex_iterator(self):
		file_data = self.srt_contents[self.index['gnss']:]
		
		if self.connect_to_hycom(): 
			for counter, line in enumerate(file_data, self.index['gnss']):
				if line == '\n' or line[0] == '#': #skip non-data lines
					pass
				else:
					line = line.split()
					#retrieve data from line
					self.retrieve_line_values(line)
	
					#create hycom time index for opendap server query
					datetime_list = self.format_datetime(self.srt_line_data['date_reading'],\
														 self.srt_line_data['time_reading'])
					epoch_hours = self.hours_since_epoch(*datetime_list)
					time_index = (epoch_hours - self.hycom_date_zero)/3.06
	
					#create hycom location index for opendap server query
					lat_dd = self.dms_to_dd(self.srt_line_data['latdd_reading'], \
											self.srt_line_data['latmn_reading'], \
											self.srt_line_data['latss_reading'])
					lon_dd = self.dms_to_dd(self.srt_line_data['londd_reading'], \
											self.srt_line_data['lonmn_reading'], \
											self.srt_line_data['lonss_reading'])
					lat_index = self.find_latitude_index(lat_dd)
					lon_index = self.find_longitude_index(lon_dd)
	
					#create hycom depth index for opendap server query
					depth_index = '0:39'
	
					#final query
					hycom_query = [time_index, depth_index, lat_index, lon_index] #raw values
					hycom_query = [int(time_index), depth_index, int(lat_index), int(lon_index)] #rounded floor
	
					#query the model for line data
					if hycom_query in self.hycom_query_cache:
						pass
					else:
						self.hycom_query_cache.append(hycom_query)
						self.query_hycom_salinity()
						if self.hycom_query_flag[-1]:
							self.successful_query_srt_index.append(counter)
							self.raw_latdd_londd.append((lat_dd, lon_dd))
	
					#reset dictionary values
					self.srt_line_data = dict.fromkeys(self.srt_line_data,0)

		else:
			if self.rinex_iterator_retry_count == self.rinex_iterator_retry_attempts:
				print "ERROR: failed to connect to hycom server after {} tries".format(self.rinex_iterator_retry_attempts)
			else:
				self.rinex_iterator_retry_count += 1
				self.rinex_iterator()

		#if no results were found, perform radial search for data
		if not self.hycom_query_flag: #fix, will execute search based on last hycom query in cache; can query each value in cache and average svp, fix, only append queries successful
			self.search_hycom()
		
		#take successful queries and get temperature values
		self.query_hycom_temperature()

		#save queried data as caris svp
		self.save_output_svp()


	#helper: retrieves needed values from rinex line
	#saves values to slf.srt_line_data
	def retrieve_line_values(self,line):
		for k,v in self.srt_line_map_values.items():
			if k == 'date_reading' or k == 'time_reading':
				index_key = self.srt_line_map_values[k]
				index_value = self.header_index[index_key]
				self.srt_line_data[k] = line[index_value]
			else:
				index_key = self.srt_line_map_values[k]
				index_value = self.header_index[index_key]
				self.srt_line_data[k] = float(line[index_value])

	#helper: format rinex date and time into ordered list
	def format_datetime(self, date, time):
		format_date = date.split('-')
		format_date = map(int, format_date)
		format_time = time.split(':')
		format_time = map(float, format_time)
		format_time = map(int, format_time)
		return format_date+format_time

	#helper: convert date and time to hours since hycom epoch
	def hours_since_epoch(self, year, month, day, hours, mins, secs):
		now = datetime(year, month, day, hours, mins, secs)
		difference = now - self.hycom_epoch
		days, seconds = difference.days, difference.seconds
		hours = days * 24 + seconds // 3600
		return hours

	#helper: covert dms location to decimal degree
	def dms_to_dd(self, dd, mn, ss):
		decdegree = dd + (mn/60) + (ss/3600)
		return decdegree

	#helper: returns hycom index for given latitude
	def find_latitude_index(self, latitude):
		#function constants
		hycom_lower_lat = -80
		hycom_upper_lat = 40
		polar_step = 0.04
		non_polar_step = 0.08
	
		#determine which range in hycom grid latitude is in and return index
		#lower range (-80)-(-40) @0.04
		if latitude <= -40: 
			latitude = (latitude - hycom_lower_lat) / polar_step
			return latitude
		
		#upper range (40)-(90) @0.04
		elif latitude >= 40:
			latitude = (latitude - hycom_upper_lat) / polar_step
			return latitude + 2000 
		
		else:
		#mid range (-40)-(40) @0.08
			if latitude == 0:
				return 1500
			elif latitude <0:
				latitude = (latitude + hycom_upper_lat) / non_polar_step
				return latitude + 1000
			else:
				latitude = latitude / non_polar_step
				return latitude + 1500
	
	#helper: return hycom index for given longitude
	def find_longitude_index(self, longitude):
		lon_step = 0.08
		if longitude < 0:
			return (longitude + 360) / lon_step
		else:
			return longitude / lon_step

	#helper: connect to hycom model opendap server
	#create database handle and set global
	def connect_to_hycom(self):
		try:
			self.hycom_db_handle = open_url(self.gbl_hycom)
			return True
		except:
			conn_error = "ConnectionError: Could not connect to Hycom Server URL {}".format(self.gbl_hycom)
			print conn_error
			return False

	#helper: query salinity values from hycom model
	def query_hycom_salinity(self):
		dataset = self.hycom_db_handle.salinity
		query = self.hycom_query_cache[-1]
		salinity = dataset['salinity'][query[0],0:39,query[2],query[3]] #depth returns syntax error when using string
		if not salinity[0][0][0] == -30000:
			self.hycom_query_flag.append(True)
			self.hycom_salinity_data.append(salinity)
		else:
			self.hycom_query_flag.append(False)

	#helper: query temperature values from hycom model
	def query_hycom_temperature(self):
		dataset = self.hycom_db_handle.water_temp
		query = self.hycom_query_cache
		flag = self.hycom_query_flag
		for flag,query in zip(flag,query):
			if flag:
				temperature = dataset['water_temp'][query[0],0:39,query[2],query[3]] #depth returns syntax error when using string
				if not temperature[0][0][0] == -30000:
					self.hycom_temperature_data.append(temperature)

	#helper: find nearest node with values using radial search
	def search_hycom(self):
		query = self.hycom_query_cache
		flag = self.hycom_query_flag
		for flag,query in zip(flag,query):
			if not flag:
				counter = [1, 1, 1, 1, 1, 1, 1, 1]
				index = 0
				while not self.hycom_query_flag[-1]:
					if index == 0:
						query[2] = query[2] + counter[index]
						self.hycom_query_cache.append(query)
						self.query_hycom_salinity()
						if not self.hycom_query_flag[-1]:
							self.hycom_query_cache.pop()
							self.hycom_query_flag.pop()
						counter[index] += 1
						index += 1
					elif index == 1:
						query[2] = query[2] - counter[index]
						self.hycom_query_cache.append(query)
						self.query_hycom_salinity()
						if not self.hycom_query_flag[-1]:
							self.hycom_query_cache.pop()
							self.hycom_query_flag.pop()
						counter[index] += 1
						index += 1
					elif index == 2:
						query[3] = query[3] + counter[index]
						self.hycom_query_cache.append(query)
						self.query_hycom_salinity()
						if not self.hycom_query_flag[-1]:
							self.hycom_query_cache.pop()
							self.hycom_query_flag.pop()
						counter[index] += 1
						index += 1
					elif index == 3:
						query[3] = query[3] - counter[index]
						self.hycom_query_cache.append(query)
						self.query_hycom_salinity()
						if not self.hycom_query_flag[-1]:
							self.hycom_query_cache.pop()
							self.hycom_query_flag.pop()
						counter[index] += 1
						index += 1
					elif index == 4:
						query[2] = query[2] + counter[index]
						query[3] = query[3] + counter[index]
						self.hycom_query_cache.append(query)
						self.query_hycom_salinity()
						if not self.hycom_query_flag[-1]:
							self.hycom_query_cache.pop()
							self.hycom_query_flag.pop()
						counter[index] += 1
						index += 1
					elif index == 5:
						query[2] = query[2] - counter[index]
						query[3] = query[3] - counter[index]
						self.hycom_query_cache.append(query)
						self.query_hycom_salinity()
						if not self.hycom_query_flag[-1]:
							self.hycom_query_cache.pop()
							self.hycom_query_flag.pop()
						counter[index] += 1
						index += 1
					elif index == 6:
						query[2] = query[2] + counter[index]
						query[3] = query[3] - counter[index]
						self.hycom_query_cache.append(query)
						self.query_hycom_salinity()
						if not self.hycom_query_flag[-1]:
							self.hycom_query_cache.pop()
							self.hycom_query_flag.pop()
						counter[index] += 1
						index += 1
					else:
						query[2] = query[2] - counter[index]
						query[3] = query[3] + counter[index]
						self.hycom_query_cache.append(query)
						self.query_hycom_salinity()
						if not self.hycom_query_flag[-1]:
							self.hycom_query_cache.pop()
							self.hycom_query_flag.pop()
						counter[index] += 1
						index = 0

	#helper: save queried data to svp caris format
	def save_output_svp(self):
		salinity = self.hycom_salinity_data
		temperature = self.hycom_temperature_data
		self.clean_directory()
		for count, (sal,temp) in enumerate(zip(salinity,temperature)):
			new_file_name = "{}_".format(count) + self.srt_file_name.split(".")[0] + ".svp"
			svp_file_path = self.output_path + new_file_name
			fn = open(svp_file_path, "w")
			fn.write('[SVP_VERSION_2]\n')
			fn.write(new_file_name + '\n')
			fn.write(self.format_svp_header(count))
			lat = self.raw_latdd_londd[count][0]
			lon = self.raw_latdd_londd[count][1]
			svp = self.calculate_svp(lat, lon)
			for d_sv in svp:
				fn.write('{}	{}\n'.format(d_sv[0], d_sv[1]))
			fn.close()

	#helper: removes all .svp files if exists
	def clean_directory(self):
		for file in os.listdir(self.output_path):
			if file.endswith('.svp'):
				os.remove(os.path.join(self.output_path, file))

	#helper: format header line of svp file
	def format_svp_header(self, count):
		srt_line = self.srt_contents[self.successful_query_srt_index[count]]
		srt_line = srt_line.split()
		year = srt_line[self.header_index['date_index']].split('-')[0]
		doy = int(float(srt_line[self.header_index['doy_index']]))
		time = srt_line[self.header_index['time_index']]
		lat = '{}:{}:{}'.format(\
			 srt_line[self.header_index['latdd_index']],\
			 srt_line[self.header_index['latmn_index']],\
			 srt_line[self.header_index['latss_index']])
		lon = '{}:{}:{}'.format(\
			 srt_line[self.header_index['londd_index']],\
			 srt_line[self.header_index['lonmn_index']],\
			 srt_line[self.header_index['lonss_index']])
		#calculate srt_lines svp applied to
		if count == len(self.successful_query_srt_index)-1:
			self.successful_query_srt_index.append(len(self.srt_contents)-1)
		upper_idx = self.successful_query_srt_index[count]
		lower_idx = self.successful_query_srt_index[-1]
		query = ','.join(map(str,self.hycom_query_cache[count]))
		comment = 'SRT[{}:{}];'.format(upper_idx, lower_idx) + "Query:{}".format(query)
		comment = 'Section {}-{} {} {} {} '.format(year, doy, time, lat, lon) + comment
		return comment

	#helper: calculate svp from Teos-10 formula
	#utilizes the gsw library to do calculation
	def calculate_svp(self, lat, lon):
		salinity = self.hycom_salinity_data
		temperature = self.hycom_temperature_data
		output_svp = [] #list of tuples(depth, sv)
		for count, (sal,temp) in enumerate(zip(salinity[0][0],temperature[0][0])):
			if sal == -30000 or temp == -30000:
				return output_svp
			else:
				sal = (int(sal) * 0.001) +20 #convert from hycom value to real value
				temp = (int(temp) * 0.001) +20 #convert from hycom value to real value
				depth = self.hycom_depth_array[count]
				s_abs = gsw.SA_from_SP(sal, depth, lon, lat) #absolute salinity from practical salinity, pressure, lon, lat
				sv = gsw.sound_speed(s_abs, temp, depth)
				output_svp.append((depth, sv))


#notes:
#add logging
#add documentation
#add testing
#add error handling (timeout on salinity)

def check_for_args():
	if len(sys.argv) < 3:
		return False
	return True
if __name__ == "__main__":
	if check_for_args():
		svp = Hycom_SVP_Query(sys.argv[1], sys.argv[2])
		svp.load_srt_contents()
		svp.identify_srt_header()
		svp.identify_header_variables()
		svp.rinex_iterator()
	else:
		print "[+] No arguments provided."
		print "[+]  "
		print "[+] ------- Usages -------"
		print "[+] python hycom_svp.py 'srt file' 'work_directory'"
		print "[+]  "
		print "[+] And also, for it to work, python need to run this file"
		print "[+] within the directory #CSB_Processing_Scripts/3.SVP"

'''svp = Hycom_SVP_Query('16_32_34-2018_08_02-gps.srt','C:/PPP/work/')
svp.load_srt_contents()
svp.identify_srt_header()
svp.identify_header_variables()
svp.rinex_iterator()'''
print "COMPLETE"
#import pdb; pdb.set_trace()