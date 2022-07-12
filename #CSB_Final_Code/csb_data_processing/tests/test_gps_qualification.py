import os
import unittest
from gps_qualification import apply_nrcan_ppp, qualify_ppp_output

class gps_TestCase(unittest.TestCase):
    """Tests for `gps_qualification.py`."""

    def test_apply_nrcan_ppp(self):
        """tests output of NRCAN PPP"""
        rnx_file = "test_output.17o"
        output_path = "C:/PPP/Test/"

        ##Test Setup##

        #delete output_path or make it
        try:  
            os.rmdir(output_path)
        except OSError:  
            print ("Deletion of the directory %s failed" % output_path)

        try:  
            os.mkdir(output_path)
        except OSError:  
            print ("Creation of the directory %s failed" % output_path)

        #remove all file in directory
        current_directory_files = os.listdir(output_path)
        for file in current_directory_files:
            os.remove(os.path.join(output_path, file))

        #False Setup
        fake_rnx_file = 'fake_'+rnx_file
        with open(os.path.join(output_path, fake_rnx_file), 'w'):
            pass
        false_path = apply_nrcan_ppp(rnx_file, output_path+ "Fake")
        self.assertTrue("IOError:" in false_path)
        false_file = apply_nrcan_ppp(rnx_file, output_path)
        self.assertTrue("IOError:" in false_file)

        #True Setup
        with open(os.path.join(output_path, rnx_file), 'w'):
            pass
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(os.path.exists(output_path+rnx_file))

        #create fake nrcan script
        with open(output_path+"test_csrs_ppp_cgi_browser.py", 'w') as fd:
            fd.write("return 0 \n")
            fd.close()

        response = apply_nrcan_ppp(rnx_file, output_path, "test_csrs_ppp_cgi_browser.py")
        import pdb;pdb.set_trace()



if __name__ == '__main__':
    unittest.main()

#test using small rinex file