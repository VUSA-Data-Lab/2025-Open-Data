package com.universityProject.demo.model;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@AllArgsConstructor
@NoArgsConstructor
@Setter
@Getter
public class TrafficAccidents{
	@JsonProperty("registrokodas")
	private String recordCode;
	@JsonProperty("dataLaikas")
	private String dateTime;
	@JsonProperty("registravimoData")
	private String registerDate;
	@JsonProperty("paskutinioRedagavimoLaikas")
	private String lastEditTime;
	@JsonProperty("iskaitinis")
	private int finalA;
	@JsonProperty("rusis")
	private String type;
	@JsonProperty("schema1")
	private String scheme1;
	@JsonProperty("schema2")
	private String scheme2;
	@JsonProperty("dalyviuSkaicius")
	private int numberOfParticipants;
	@JsonProperty("zuvusiuSkaicius")
	private int numberOfFatalities;
	@JsonProperty("zuvVaiku")
	private int childrenKilled;
	@JsonProperty("suzeistuSkaicius")
	private int numberOfInjured;
	@JsonProperty("suzeistaVaiku")
	private int childrenInjured;
	@JsonProperty("tpSkaicius")
	private int numberOfVehicles;
	@JsonProperty("policijosTpSkaicius")
	private int numberOfPoliceVehicles;
	@JsonProperty("apgadintuTpSkaicius")
	private int numberOfDamagedVehicles;
	@JsonProperty("apgadintuPolicijosTpSkaicius")
	private int numberOfDamagedPoliceVehicles;
	@JsonProperty("policijosIstaigaL1")
	private String policeDepartmentL1;
	@JsonProperty("policijosIstaigaL2")
	private String policeDepartmentL2;
	@JsonProperty("iforminusiIstaigaL1")
	private String registeredByL1;
	@JsonProperty("iforminusiIstaigaL2")
	private String registeredByL2;
	@JsonProperty("ivykioVieta")
	private String incidentLocation;
	@JsonProperty("vietosSavivaldybeTipas")
	private String municipalityType;
	@JsonProperty("savivaldybe")
	private String municipality;
	@JsonProperty("gatve")
	private String street;
	@JsonProperty("namas")
	private String houseNumber;
	@JsonProperty("kitaGatveSankryzoje")
	private String otherStreetAtIntersection;
	@JsonProperty("kelioPavadinimas")
	private String roadName;
	@JsonProperty("kelioReiksme")
	private String roadType;
	@JsonProperty("atstumas")
	private String distance;
	@JsonProperty("dangosRusis")
	private String roadSurfaceType;
	@JsonProperty("dangosBukle")
	private String roadSurfaceCondition;
	@JsonProperty("parosMetas")
	private String timeOfDay;
	@JsonProperty("kelioApsvietimas")
	private String roadLighting;
	@JsonProperty("meteoSalygos")
	private String weatherCondition;
	@JsonProperty("kitosOroSalygos")
	private String[] otherWeatherConditions;
	@JsonProperty("kelioGatvesKreive")
	private String roadCurve;
	@JsonProperty("nuliamentisVeiksnys")
	private String mainContributingFactor;
	@JsonProperty("kitiNuliamentysVeiksniai")
	private String[] otherContributingFactors;
	@JsonProperty("atitvarai")
	private String roadBarriers;
	@JsonProperty("sankryzosTipas")
	private String intersectionType;
	@JsonProperty("kelioElementas1")
	private String roadElement1;
	@JsonProperty("kelioElementas2")
	private String roadElement2;
	@JsonProperty("privalomasLeistinasGreitis")
	private String mandatorySpeedLimit;
	@JsonProperty("leistinasGreitis")
	private double speedLimit;
	@JsonProperty("neblaivusKaltininkai")
	private String drunkOffenders;
	@JsonProperty("apsvaigeKaltininkai")
	private String intoxicatedOffenders;
	@JsonProperty("atsisakeTikrintisKaltininkai")
	private String refusedTestingOffenders;
	@JsonProperty("ilguma")
	private double longitude;
	@JsonProperty("platuma")
	private double latitude;
	@JsonProperty("eismoDalyviai")
	private List<TrafficParticipants> trafficParticipants;
	@JsonProperty("eismoTranspPreimone")
	private List<TrafficVehicles> traficVehicles;
	
	public TrafficAccidents() {
		
	}
	
	public TrafficAccidents(String recordCode, String dateTime, String registerDate, String lastEditTime, int finalA,
			String type, String scheme1, String scheme2, int numberOfParticipants, int numberOfFatalities,
			int childrenKilled, int numberOfInjured, int childrenInjured, int numberOfVehicles,
			int numberOfPoliceVehicles, int numberOfDamagedVehicles, int numberOfDamagedPoliceVehicles,
			String policeDepartmentL1, String policeDepartmentL2, String registeredByL1, String registeredByL2,
			String incidentLocation, String municipalityType, String municipality, String street, String houseNumber,
			String otherStreetAtIntersection, String roadName, String roadType, String distance, String roadSurfaceType,
			String roadSurfaceCondition, String timeOfDay, String roadLighting, String weatherCondition,
			String[] otherWeatherConditions, String roadCurve, String mainContributingFactor,
			String[] otherContributingFactors, String roadBarriers, String intersectionType, String roadElement1,
			String roadElement2, String mandatorySpeedLimit, double speedLimit, String drunkOffenders,
			String intoxicatedOffenders, String refusedTestingOffenders, double longitude, double latitude,
			List<TrafficParticipants> trafficParticipants, List<TrafficVehicles> traficVehicles) {
		
		this.recordCode = recordCode;
		this.dateTime = dateTime;
		this.registerDate = registerDate;
		this.lastEditTime = lastEditTime;
		this.finalA = finalA;
		this.type = type;
		this.scheme1 = scheme1;
		this.scheme2 = scheme2;
		this.numberOfParticipants = numberOfParticipants;
		this.numberOfFatalities = numberOfFatalities;
		this.childrenKilled = childrenKilled;
		this.numberOfInjured = numberOfInjured;
		this.childrenInjured = childrenInjured;
		this.numberOfVehicles = numberOfVehicles;
		this.numberOfPoliceVehicles = numberOfPoliceVehicles;
		this.numberOfDamagedVehicles = numberOfDamagedVehicles;
		this.numberOfDamagedPoliceVehicles = numberOfDamagedPoliceVehicles;
		this.policeDepartmentL1 = policeDepartmentL1;
		this.policeDepartmentL2 = policeDepartmentL2;
		this.registeredByL1 = registeredByL1;
		this.registeredByL2 = registeredByL2;
		this.incidentLocation = incidentLocation;
		this.municipalityType = municipalityType;
		this.municipality = municipality;
		this.street = street;
		this.houseNumber = houseNumber;
		this.otherStreetAtIntersection = otherStreetAtIntersection;
		this.roadName = roadName;
		this.roadType = roadType;
		this.distance = distance;
		this.roadSurfaceType = roadSurfaceType;
		this.roadSurfaceCondition = roadSurfaceCondition;
		this.timeOfDay = timeOfDay;
		this.roadLighting = roadLighting;
		this.weatherCondition = weatherCondition;
		this.otherWeatherConditions = otherWeatherConditions;
		this.roadCurve = roadCurve;
		this.mainContributingFactor = mainContributingFactor;
		this.otherContributingFactors = otherContributingFactors;
		this.roadBarriers = roadBarriers;
		this.intersectionType = intersectionType;
		this.roadElement1 = roadElement1;
		this.roadElement2 = roadElement2;
		this.mandatorySpeedLimit = mandatorySpeedLimit;
		this.speedLimit = speedLimit;
		this.drunkOffenders = drunkOffenders;
		this.intoxicatedOffenders = intoxicatedOffenders;
		this.refusedTestingOffenders = refusedTestingOffenders;
		this.longitude = longitude;
		this.latitude = latitude;
		this.trafficParticipants = trafficParticipants;
		this.traficVehicles = traficVehicles;
	}

	public String getRecordCode() {
		return recordCode;
	}

	public void setRecordCode(String recordCode) {
		this.recordCode = recordCode;
	}

	public String getDateTime() {
		return dateTime;
	}

	public void setDateTime(String dateTime) {
		this.dateTime = dateTime;
	}

	public String getRegisterDate() {
		return registerDate;
	}

	public void setRegisterDate(String registerDate) {
		this.registerDate = registerDate;
	}

	public String getLastEditTime() {
		return lastEditTime;
	}

	public void setLastEditTime(String lastEditTime) {
		this.lastEditTime = lastEditTime;
	}

	public int getFinalA() {
		return finalA;
	}

	public void setFinalA(int finalA) {
		this.finalA = finalA;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public String getScheme1() {
		return scheme1;
	}

	public void setScheme1(String scheme1) {
		this.scheme1 = scheme1;
	}

	public String getScheme2() {
		return scheme2;
	}

	public void setScheme2(String scheme2) {
		this.scheme2 = scheme2;
	}

	public int getNumberOfParticipants() {
		return numberOfParticipants;
	}

	public void setNumberOfParticipants(int numberOfParticipants) {
		this.numberOfParticipants = numberOfParticipants;
	}

	public int getNumberOfFatalities() {
		return numberOfFatalities;
	}

	public void setNumberOfFatalities(int numberOfFatalities) {
		this.numberOfFatalities = numberOfFatalities;
	}

	public int getChildrenKilled() {
		return childrenKilled;
	}

	public void setChildrenKilled(int childrenKilled) {
		this.childrenKilled = childrenKilled;
	}

	public int getNumberOfInjured() {
		return numberOfInjured;
	}

	public void setNumberOfInjured(int numberOfInjured) {
		this.numberOfInjured = numberOfInjured;
	}

	public int getChildrenInjured() {
		return childrenInjured;
	}

	public void setChildrenInjured(int childrenInjured) {
		this.childrenInjured = childrenInjured;
	}

	public int getNumberOfVehicles() {
		return numberOfVehicles;
	}

	public void setNumberOfVehicles(int numberOfVehicles) {
		this.numberOfVehicles = numberOfVehicles;
	}

	public int getNumberOfPoliceVehicles() {
		return numberOfPoliceVehicles;
	}

	public void setNumberOfPoliceVehicles(int numberOfPoliceVehicles) {
		this.numberOfPoliceVehicles = numberOfPoliceVehicles;
	}

	public int getNumberOfDamagedVehicles() {
		return numberOfDamagedVehicles;
	}

	public void setNumberOfDamagedVehicles(int numberOfDamagedVehicles) {
		this.numberOfDamagedVehicles = numberOfDamagedVehicles;
	}

	public int getNumberOfDamagedPoliceVehicles() {
		return numberOfDamagedPoliceVehicles;
	}

	public void setNumberOfDamagedPoliceVehicles(int numberOfDamagedPoliceVehicles) {
		this.numberOfDamagedPoliceVehicles = numberOfDamagedPoliceVehicles;
	}

	public String getPoliceDepartmentL1() {
		return policeDepartmentL1;
	}

	public void setPoliceDepartmentL1(String policeDepartmentL1) {
		this.policeDepartmentL1 = policeDepartmentL1;
	}

	public String getPoliceDepartmentL2() {
		return policeDepartmentL2;
	}

	public void setPoliceDepartmentL2(String policeDepartmentL2) {
		this.policeDepartmentL2 = policeDepartmentL2;
	}

	public String getRegisteredByL1() {
		return registeredByL1;
	}

	public void setRegisteredByL1(String registeredByL1) {
		this.registeredByL1 = registeredByL1;
	}

	public String getRegisteredByL2() {
		return registeredByL2;
	}

	public void setRegisteredByL2(String registeredByL2) {
		this.registeredByL2 = registeredByL2;
	}

	public String getIncidentLocation() {
		return incidentLocation;
	}

	public void setIncidentLocation(String incidentLocation) {
		this.incidentLocation = incidentLocation;
	}

	public String getMunicipalityType() {
		return municipalityType;
	}

	public void setMunicipalityType(String municipalityType) {
		this.municipalityType = municipalityType;
	}

	public String getMunicipality() {
		return municipality;
	}

	public void setMunicipality(String municipality) {
		this.municipality = municipality;
	}

	public String getStreet() {
		return street;
	}

	public void setStreet(String street) {
		this.street = street;
	}

	public String getHouseNumber() {
		return houseNumber;
	}

	public void setHouseNumber(String houseNumber) {
		this.houseNumber = houseNumber;
	}

	public String getOtherStreetAtIntersection() {
		return otherStreetAtIntersection;
	}

	public void setOtherStreetAtIntersection(String otherStreetAtIntersection) {
		this.otherStreetAtIntersection = otherStreetAtIntersection;
	}

	public String getRoadName() {
		return roadName;
	}

	public void setRoadName(String roadName) {
		this.roadName = roadName;
	}

	public String getRoadType() {
		return roadType;
	}

	public void setRoadType(String roadType) {
		this.roadType = roadType;
	}

	public String getDistance() {
		return distance;
	}

	public void setDistance(String distance) {
		this.distance = distance;
	}

	public String getRoadSurfaceType() {
		return roadSurfaceType;
	}

	public void setRoadSurfaceType(String roadSurfaceType) {
		this.roadSurfaceType = roadSurfaceType;
	}

	public String getRoadSurfaceCondition() {
		return roadSurfaceCondition;
	}

	public void setRoadSurfaceCondition(String roadSurfaceCondition) {
		this.roadSurfaceCondition = roadSurfaceCondition;
	}

	public String getTimeOfDay() {
		return timeOfDay;
	}

	public void setTimeOfDay(String timeOfDay) {
		this.timeOfDay = timeOfDay;
	}

	public String getRoadLighting() {
		return roadLighting;
	}

	public void setRoadLighting(String roadLighting) {
		this.roadLighting = roadLighting;
	}

	public String getWeatherCondition() {
		return weatherCondition;
	}

	public void setWeatherCondition(String weatherCondition) {
		this.weatherCondition = weatherCondition;
	}

	public String[] getOtherWeatherConditions() {
		return otherWeatherConditions;
	}

	public void setOtherWeatherConditions(String[] otherWeatherConditions) {
		this.otherWeatherConditions = otherWeatherConditions;
	}

	public String getRoadCurve() {
		return roadCurve;
	}

	public void setRoadCurve(String roadCurve) {
		this.roadCurve = roadCurve;
	}

	public String getMainContributingFactor() {
		return mainContributingFactor;
	}

	public void setMainContributingFactor(String mainContributingFactor) {
		this.mainContributingFactor = mainContributingFactor;
	}

	public String[] getOtherContributingFactors() {
		return otherContributingFactors;
	}

	public void setOtherContributingFactors(String[] otherContributingFactors) {
		this.otherContributingFactors = otherContributingFactors;
	}

	public String getRoadBarriers() {
		return roadBarriers;
	}

	public void setRoadBarriers(String roadBarriers) {
		this.roadBarriers = roadBarriers;
	}

	public String getIntersectionType() {
		return intersectionType;
	}

	public void setIntersectionType(String intersectionType) {
		this.intersectionType = intersectionType;
	}

	public String getRoadElement1() {
		return roadElement1;
	}

	public void setRoadElement1(String roadElement1) {
		this.roadElement1 = roadElement1;
	}

	public String getRoadElement2() {
		return roadElement2;
	}

	public void setRoadElement2(String roadElement2) {
		this.roadElement2 = roadElement2;
	}

	public String getMandatorySpeedLimit() {
		return mandatorySpeedLimit;
	}

	public void setMandatorySpeedLimit(String mandatorySpeedLimit) {
		this.mandatorySpeedLimit = mandatorySpeedLimit;
	}

	public double getSpeedLimit() {
		return speedLimit;
	}

	public void setSpeedLimit(double speedLimit) {
		this.speedLimit = speedLimit;
	}

	public String getDrunkOffenders() {
		return drunkOffenders;
	}

	public void setDrunkOffenders(String drunkOffenders) {
		this.drunkOffenders = drunkOffenders;
	}

	public String getIntoxicatedOffenders() {
		return intoxicatedOffenders;
	}

	public void setIntoxicatedOffenders(String intoxicatedOffenders) {
		this.intoxicatedOffenders = intoxicatedOffenders;
	}

	public String getRefusedTestingOffenders() {
		return refusedTestingOffenders;
	}

	public void setRefusedTestingOffenders(String refusedTestingOffenders) {
		this.refusedTestingOffenders = refusedTestingOffenders;
	}

	public double getLongitude() {
		return longitude;
	}

	public void setLongitude(double longitude) {
		this.longitude = longitude;
	}

	public double getLatitude() {
		return latitude;
	}

	public void setLatitude(double latitude) {
		this.latitude = latitude;
	}

	public List<TrafficParticipants> getTrafficParticipants() {
		return trafficParticipants;
	}

	public void setTrafficParticipants(List<TrafficParticipants> trafficParticipants) {
		this.trafficParticipants = trafficParticipants;
	}

	public List<TrafficVehicles> getTraficVehicles() {
		return traficVehicles;
	}

	public void setTraficVehicles(List<TrafficVehicles> traficVehicles) {
		this.traficVehicles = traficVehicles;
	}

}