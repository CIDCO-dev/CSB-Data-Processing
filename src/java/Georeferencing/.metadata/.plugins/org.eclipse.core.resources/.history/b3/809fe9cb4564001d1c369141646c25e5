package ca.cidco.csb.surveydata;

import java.sql.Timestamp;

public class Attitude{
	
	private Timestamp timestamp;
	
	private Double heading; //in degrees
	private Double pitch;   //in degrees
	private Double roll;    //in degrees
	
	
	public Attitude(Timestamp timestamp_, Double heading_, Double pitch_, Double roll_) {
		timestamp = timestamp_;
		heading = heading_;
		pitch = pitch_;
		roll = roll_;
	}
	
	public Timestamp getTimestamp() {
		return timestamp;
	}
	public void setTimestamp(Timestamp timestamp) {
		this.timestamp = timestamp;
	}
	public Double getHeading() {
		return heading;
	}
	public void setHeading(Double heading) {
		this.heading = heading;
	}
	public Double getPitch() {
		return pitch;
	}
	public void setPitch(Double pitch) {
		this.pitch = pitch;
	}
	public Double getRoll() {
		return roll;
	}
	public void setRoll(Double roll) {
		this.roll = roll;
	}
    // Overriding toString() method of String class
    @Override
    public String toString() {
        return "timestamp : "+ timestamp+" |  heading : "+ heading+" |  Pitch : "+pitch+" Roll "+ roll +"\n";
    }
	
}
