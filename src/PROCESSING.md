For each CSB data bundle (sonar file, IMU file, GNSS text file, GNSS binary file):

	1) Generate RINEX file from GNSS binary file using convbin (from ubx or other binary files)
	2) Using the RINEX, we get a PPP position file
	3) Qualify the PPP -> Pass or Fail. Use GDOP, # of satellites, SD (as parameters)
	4) Interpolate and Georeference
		a)If GNSS qualification Pass, we do ERS

		b)If GNSS qualification Fail, do WLRS (TBD)
