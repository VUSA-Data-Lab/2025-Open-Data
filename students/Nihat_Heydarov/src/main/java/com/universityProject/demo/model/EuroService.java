package com.universityProject.demo.model;

public class EuroService{
	private String geo;
	private String purchases;
	private String time;
	private String timeFrequency;
	private String unitMeasure;
	private Double value;
	
	public EuroService(String geo,String purchases,String time,String timeFrequency,String unitMeasure,Double value) {
		this.geo = geo;
		this.purchases = purchases;
		this.time = time;
		this.timeFrequency = timeFrequency;
		this.unitMeasure = unitMeasure;
		this.value = value;
	}
	
	public EuroService() {
		
	}
	
	public void setGeo(String geo) {
		this.geo = geo;
	}
	public String getGeo() {
		return geo;
	}
	public void setPurchases(String purchases) {
		this.purchases = purchases;
	}
	public String getPurchases() {
		return purchases;
	}
	public void setTime(String time) {
		this.time = time;
	}
	public String getTime() {
		return time;
	}
	public void setValue(Double value) {
		this.value = value;
	}
	public Double getValue() {
		return value;
	}
	public void setTimeFrequency(String timeFrequency) {
		this.timeFrequency = timeFrequency;
	}
	public String getTimeFrequency() {
		return timeFrequency;
	}
	public void setUnitMeasure(String unitMeasure) {
		this.unitMeasure = unitMeasure;
	}
	public String getUnitMeasure() {
		return unitMeasure;
	}
	
}