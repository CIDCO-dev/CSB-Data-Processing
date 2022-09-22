import os
import json
from pydap.client import open_url

'''
Used to store time index values for the Hycom Model. Needed because the time indices are not uniform as
the model has missing data for certain date ranges. As a result there is not mathematical way to calculate
the index value for a particular date/time precisely. 

Lookup table stored as a dictionary for quick lookup times. As the time index value max is always increasing, 
the lookup table must be periodically updated to include latest time values. 

Lookup table stores the hours since epoch as the key and the hycom index value as the value. 

'''

class Hycom_Lookup_Update:

	#store url and respective lookup tables here and change in __init__ accordingly
	gbl_hycom_93_url = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_93.0'
	hycom_lookup_table_93 = 'lookup_table_93.txt'

	def __init__(self):

		#set to preferred url and lookup table
		self.hycom_url = self.gbl_hycom_93_url
		self.lookup_table_name = self.hycom_lookup_table_93
		self.lookup_table = ''
		self.load_lookup_table()
		self.retry_attempts = 0
		self.hycom_db_handle = self.connect_to_hycom()
		if self.hycom_db_handle != False:
			self.hycom_db_handle = self.hycom_db_handle.time
			self.latest_data_gap = (max(self.lookup_table.values()), self.hycom_db_handle.shape[0])
			self.lookup_table_update()
		else:
			print 'UNSUCCESSFULLY UPDATED HYCOM LOOKUP TABLE'

	#load the lookup table from txt to memory
	def load_lookup_table(self):
		file = self.lookup_table_name
		if os.path.exists(file):
				if os.stat(file).st_size == 0:
					os.remove(file)
					self.load_lookup_table(file)
				else:
					with open(self.lookup_table_name, 'r') as f:
						hycom_lookup_table = eval(f.read())
						self.lookup_table = hycom_lookup_table
						print 'successfully loaded lookup table'			
		else:
			print "lookup table non-existant...creating"
			t0 = {157812: 0} #hardcoded t=0 for expt93, change if using other
			json.dump(t0, open(self.lookup_table_name, 'w'))
			self.load_lookup_table()


	#create database handle and set global
	def connect_to_hycom(self):
		url = self.hycom_url
		print 'attempting to connect to Hycom url {}'.format(url)
		try:
			hycom_db_handle = open_url(url)
			print 'successfully conected to Hycom url {}'.format(url)
			return hycom_db_handle
		except:
			conn_error = "ConnectionError: Could not connect to Hycom Server URL {}".format(url)
			print conn_error
			return False

	#queries all missing data up to the latest hycom time index
	def lookup_table_update(self):
		dataset = self.hycom_db_handle
		query_range = self.latest_data_gap
		min_value = query_range[0]
		max_value = query_range[1]
		file = self.lookup_table_name

		#query hycom for the missing time data
		print 'querying hycom for data range ({}-{})'.format(min_value, max_value)
		try:
			time = dataset[min_value:max_value]
			print 'successfully queried time range'
		except:
			print 'query was unsuccessful'
			self.retry_attempts +=1
			if self.retry_attempts < 5:
				self.lookup_table_update()
			else:
				print 'UNSECCESSFULLY QUERIED HYCOM 5X, ABORTING'
				return

		#add missing data to the lookup table
		for hours_since_epoch, hycom_index in zip(time, range(min_value, max_value+1)):
			self.lookup_table[int(hours_since_epoch)]=hycom_index

		#write back to file and close
		json.dump(self.lookup_table, open(self.lookup_table_name, 'w'))
		print "updated lookup table {} successfully".format(file)

	#simply returns lookup table and converts values to int
	def return_lookup_table(self):
		lookup_table = self.lookup_table
		converted_lookup = {}
		for key, value in lookup_table.iteritems():
			converted_lookup[int(key)] = int(value)
		return converted_lookup

#Hycom_Lookup_Update()