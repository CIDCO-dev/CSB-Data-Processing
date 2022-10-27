package ca.cidco.csb.surveydata;

import java.sql.Timestamp;

import ca.cidco.csb.utilities.Conversion;

public class Position{
	
	private Timestamp timestamp;
	
	private Double longitude; //in doubles
	private Double latitude; //in doubles
	private Double height; //in degrees
	
	private Double sdLongitude; //in meters
	private Double sdLatitude; //in meters
	private Double sdHeight; //in meters	

	private Long numberOfSatellites;
	private Double gdop;	
	
	public Position(Timestamp timestamp_, Double longitude_DD, Double longitude_MN, Double longitude_SS, Double latitude_DD , Double latitude_MN , Double latitude_SS, Double height_, Double sdLongitude_, Double sdLatitude_, Double sdHeight_, Long numberOfSatellites_, Double gdop_) {
         timestamp= timestamp_;
		 height= height_;
		 sdLongitude=  sdLongitude_;
		 sdLatitude=  sdLatitude_;
		 sdHeight=  sdHeight_;
		 numberOfSatellites=  numberOfSatellites_;
		 gdop= gdop_;
		 longitude = Conversion.convertDMStoDecimalDegree(longitude_DD, longitude_MN, longitude_SS);
		 latitude = Conversion.convertDMStoDecimalDegree(latitude_DD, latitude_MN, latitude_SS);
		 
	}
	
	public Position(Timestamp timestamp, double interpLat, double interpLon, double interpAlt, double sdLatitude, double sdLongitude, double sdHeight, long nsv, double gdop) {
		this.timestamp= timestamp;
		this.latitude= interpLat;
		this.longitude= interpLon;
		this.height= interpAlt;
		this.sdLongitude= sdLongitude;
		this.sdLatitude= sdLatitude;
		this.sdHeight= sdHeight;
		this.numberOfSatellites= nsv ;
		this.gdop= gdop;
		
		}

	public Double getLongitude() {
		return longitude;
	}

	public void setLongitude(Double longitude) {
		this.longitude = longitude;
	}

	public Double getLatitude() {
		return latitude;
	}

	public void setLatitude(Double latitude) {
		this.latitude = latitude;
	}

	public Timestamp getTimestamp() {
		return timestamp;
	}
	public void setTimestamp(Timestamp timestamp) {
		this.timestamp = timestamp;
	}


	public Double getHeight() {
		return height;
	}
	public void setHeight(Double height) {
		this.height = height;
	}
	public Double getSdLongitude() {
		return sdLongitude;
	}
	public void setSdLongitude(Double sdLongitude) {
		this.sdLongitude = sdLongitude;
	}
	public Double getSdLatitude() {
		return sdLatitude;
	}
	public void setSdLatitude(Double sdLatitude) {
		this.sdLatitude = sdLatitude;
	}
	public Double getSdHeight() {
		return sdHeight;
	}
	public void setSdHeight(Double sdHeight) {
		this.sdHeight = sdHeight;
	}
	
	public Long getNumberOfSatellites() {
		return numberOfSatellites;
	}

	public void setNumberOfSatellites(Long numberOfSatellites) {
		this.numberOfSatellites = numberOfSatellites;
	}	
	
	public Double getGdop() {
		return gdop;
	}

	public void setGdop(Double gdop) {
		this.gdop = gdop;
	}	
	
    // Overriding toString() method of String class
    @Override
    public String toString() {
        return "Timestamp : "+ timestamp+" |  Longitude : "+longitude+" | Latitude : "+ latitude +" | height : "+height +"  | NVS : "+ numberOfSatellites+" | GDOP : "+gdop + " | SDLAT : "+sdLatitude+" | SDLON : "+sdLongitude+" | SDHGT : "+sdHeight +"\n";
    }
}
