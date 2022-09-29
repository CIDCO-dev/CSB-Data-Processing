package ubx2ppp;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/*
 * To use the script, you have to install the last version of RTKLIB and put convbin in the usr/local/bin
 * Replace the pppPath value (line 21) by your NRCAN python script with his path
 * 
 * In commandline:
 * CD to this Main.java
 * Compile the change (:$ javac Main.java )
 * $java Main.java /path/to/the/file.ubx
 */


public class Main {

	
	public static void main(String[] args) throws IOException, InterruptedException {
		
        //Path to NRCAN script
		final String pppPath ="/home/dominic/eclipse_ubx/csrs_ppp_auto_v1_6_1/csrs_ppp_auto.py";		
		
		// Get file in commandline argument
        String nameFile= new java.io.File(args[0]).getName();
        String nameNoExt= nameFile.replaceAll(".ubx", "");
        String pathFile= new java.io.File(args[0]).getParent();
        
        // Make all directories 
        File name = new File (pathFile+"/"+nameNoExt);
        File Rinex = new File(pathFile+"/"+nameNoExt+"/Rinex");
        File ubx_done = new File(pathFile+"/"+nameNoExt+"/ubx_done");
        File ppp = new File(pathFile+"/"+nameNoExt+"/ppp");
        
        ArrayList<File> toMake = new ArrayList<File>(
        		Arrays.asList(name, Rinex, ubx_done, ppp));
        
        for (File file : toMake) {
        	file.mkdir();
        	}
        
        // Use convbin to generate .obs file      
        ProcessBuilder processObsBuilder= new ProcessBuilder("convbin", "-r", "ubx","-d", pathFile+"/"+nameNoExt+"/Rinex", args[0]);
        processObsBuilder.inheritIO();
        Process processOBS= processObsBuilder.start();
        processOBS.waitFor();
        
        Process moveUBX= new ProcessBuilder("mv", args[0], pathFile+"/"+nameNoExt+"/ubx_done").start();
        
        // Send .obs to NRCAN
        ProcessBuilder processBuilderPPP = new ProcessBuilder("python3", pppPath,"--user_name","dominic.gonthier@cidco.ca", "--rnx", pathFile+"/"+nameNoExt+"/Rinex/"+nameNoExt+".obs", "--results_dir", pathFile+"/"+nameNoExt+"/ppp");
        processBuilderPPP.inheritIO();
        Process processPPP= processBuilderPPP.start();
        processPPP.waitFor();

	}
}


      	
