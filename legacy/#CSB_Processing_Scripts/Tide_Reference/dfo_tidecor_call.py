'''
This module is designed to take in a list of positions and time
and query the tidecor model to obtain tidal elevation values. 

Relies on tidecor.exe provided by the DFO. 

Author: Khaleel Arfeen
Email: k.a@unb.ca
Version: 1.0.0
'''

import os 
import datetime

'''
inputs a tnav or gnav file and output
data file with appended tidal elevation
values provided from tidecor. 

'''
def query_tidecor(tidecor_path, config_file, input, output):
	


	tidecor.exe tidecor_velocity.cfg input.dat output.dat


def fetch_tidecor_output():
	pass

def update_srt():
	pass