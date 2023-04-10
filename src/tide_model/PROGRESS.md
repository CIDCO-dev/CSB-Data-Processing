In processing the time, you must becareful with the epoch you're using, so as not to have a messed up MJD.
 EG: The default epoch for .convert_datetime = (1970,1,1,0,0,0), and that of .convert_calendar_dates = (1992,1,1,0,0,0). 
 To be on a safe side, I used the pyTMD.time.epoch, which is (pyTMD.time._tide_epoch)
 
 
 I converted the time to an array to enable the predict code to read it.
 
 I think the next stage is to bring in a .pos file or .csv file, read the data, run the code and output (Time, LAT, LON, Tide) as a file.

Just added three other files for:
Processing of TPXO9-v5 model
Processing of FES Model
Processing TPXO9 or FES model
