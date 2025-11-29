package com.universityProject.demo.controller;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.ui.Model;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.core.exc.StreamReadException;
import com.fasterxml.jackson.databind.DatabindException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.universityProject.demo.model.EuroService;
import com.universityProject.demo.model.SearchObject;
import com.universityProject.demo.model.TrafficAccidents;
import com.universityProject.demo.model.TrafficParticipants;
import com.universityProject.demo.service.CsvReaderService;
import com.universityProject.demo.service.TrafficService;

@Controller
@RequestMapping("/data")
public class EuroController{
	
	
	private CsvReaderService csvReaderService;
	private TrafficService trafficService;
	
	public EuroController(CsvReaderService csvReaderService, TrafficService trafficService) {
		this.csvReaderService = csvReaderService;
		this.trafficService = trafficService;
	}
	
	
	
	
	
	
	
	
	@GetMapping("/houses")
	public String getEuroS(Model model) throws IOException{
		Map<String,EuroService> houseP = csvReaderService.readCsvFile("C://Users/Aydan/OneDrive/Desktop/prc_hpi_q_page_linear.csv");
		List<EuroService> objectsForModel = new ArrayList<>();
		houseP.forEach((k,v)-> objectsForModel.add(v));
		
		model.addAttribute("values",objectsForModel);
		return "Table";
	}
	
	@GetMapping("/traffic-accidents")
	public String getDataTrafficAccidents(Model model) throws StreamReadException, DatabindException, IOException {
		List<TrafficAccidents> data = trafficService.getData();
		List<TrafficAccidents> firstHundred = new ArrayList<>();
		for(int i=0;i<700;i++) {
			firstHundred.add(data.get(i));
		}
		
		List<String> municipalities = getMunicipality(firstHundred);
		Map<String,String> time = getTimeOfDay(firstHundred);
		List<String> timeL = new ArrayList<>();
		time.forEach((k,v)->timeL.add(v));
		
		List<String> years = getYears(firstHundred);
	    Map<String,Integer> monthsAndDays = getMonthsAndDays(firstHundred);
	    List<TrafficAccidents> firstFifty = new ArrayList<>();
	    for(int i=0;i<50;i++) {
	    	firstFifty.add(data.get(i));
	    }
	    List<String> surfaceConditions = getRoadSurfaceConditions(firstFifty);
	    int drunkCounter = getDrunkOffenders(firstFifty);
	    int intoxicatedCounter = getDrugImpairedOffenders(firstFifty);
	    int driverLicenceCounter = getDriverLicenceCount(firstFifty);
	    
		
	    model.addAttribute("trafficList", firstHundred);
	    model.addAttribute("municipalities", municipalities);
	    model.addAttribute("years", years);
	    model.addAttribute("monthsAndDays", monthsAndDays);
	    model.addAttribute("SearchObject", new SearchObject());
	    model.addAttribute("FirstFifty", firstFifty);
	    model.addAttribute("SurfaceConditions",surfaceConditions);
	    model.addAttribute("DrunkCounter",drunkCounter);
	    model.addAttribute("IntoxicatedCounter",intoxicatedCounter);
	    model.addAttribute("DriverLicenceCounter",driverLicenceCounter);
	   
	    
		
		return "TrafficAccidents";
	}
	
	@PostMapping("/traffic-accidents/search")
	public String retrieveByMunicipalityAndTime(@ModelAttribute SearchObject searchObject,Model model) throws StreamReadException, DatabindException, IOException{
		List<TrafficAccidents> data = trafficService.getData();
		List<TrafficAccidents> firstHundred = new ArrayList<>();
		for(int i=0;i<700;i++) {
			firstHundred.add(data.get(i));
		}
		Map<TrafficAccidents,String> getByMunicipality = getTrafficAccidentsByMunicipality(firstHundred);
		List<TrafficAccidents> trafficAccidents = new ArrayList<>();
		Map<TrafficAccidents,String> filteredData = new HashMap<>();
				getByMunicipality.forEach((k,v)->trafficAccidents.add(k));
				for(int i=0;i<trafficAccidents.size();i++) {
					
						String date = trafficAccidents.get(i).getDateTime();
						String dateObtain = date.substring(0,date.indexOf("-"));
						
						String municipality = trafficAccidents.get(i).getMunicipality();
								
						if(dateObtain.equals(searchObject.getYear()) && municipality.equals(searchObject.getMunicipality())) {
							filteredData.put(trafficAccidents.get(i),trafficAccidents.get(i).getDateTime());
						}
					
				}
				List<TrafficAccidents> fData = new ArrayList<>();
				filteredData.forEach((k,v)->fData.add(k));
				
				List<String> surfaceConditions = getRoadSurfaceConditions(fData);
				int drunkCounter = getDrunkOffenders(fData);
				int intoxicatedCounter = getDrugImpairedOffenders(fData);
				int driverLicenceCount = getDriverLicenceCount(fData);
				
				Map<String,Integer> retrievedData = getMonthsAndDays(fData);
				
				List<String> reason = new ArrayList<>();
				for(int i=0; i<fData.size();i++) {
					TrafficAccidents tf = new TrafficAccidents();
					
				}
				
				
			
				
				
               model.addAttribute("filteredData", retrievedData);
               model.addAttribute("AccidentDetails", fData);
               model.addAttribute("ReasonList", reason);
               model.addAttribute("RoadSurfaceConditions", surfaceConditions);
               model.addAttribute("DrunkOffenders", drunkCounter);
               model.addAttribute("IntoxicatedCounter",intoxicatedCounter);
               model.addAttribute("LicenceCount",driverLicenceCount);
               
               
               
		
     return "FilteredTrafficAccidents";
	}
	
	@GetMapping("/demo")
	@ResponseBody
	public Map<TrafficAccidents,String> getTimeOfDay() throws StreamReadException, DatabindException, IOException{
		List<TrafficAccidents> data = trafficService.getData();
		List<TrafficAccidents> firstHundred = new ArrayList<>();
		for(int i=0;i<700;i++) {
			firstHundred.add(data.get(i));
		}
		Map<TrafficAccidents,String> accidents = getTrafficAccidentsByMunicipality(firstHundred);
		return accidents;
	}
	
	private List<String> getMunicipality(List<TrafficAccidents> trafficAccidents){
		Map<String,String> municipalities = new HashMap<>();
		for(int i = 0; i<trafficAccidents.size(); i++) {
			municipalities.put(trafficAccidents.get(i).getMunicipality(), trafficAccidents.get(i).getMunicipality());
			
		}
		
		List<String> municipalitiesL = new ArrayList<>();
		
		municipalities.forEach((k,v)->municipalitiesL.add(v));
		
		
		
		return municipalitiesL;
	}
	
	private Map<String,String> getTimeOfDay(List<TrafficAccidents> firstHundred){
     Map<String,String>  dayOfTimeWithMunicipality = new HashMap<>();
     for(int i=0; i<firstHundred.size(); i++) {
    	 dayOfTimeWithMunicipality.put(firstHundred.get(i).getTimeOfDay(),firstHundred.get(i).getTimeOfDay());
     }
     return dayOfTimeWithMunicipality;
	}
	
	private List<String> getYears(List<TrafficAccidents> firstHundred){
		Map<String,String> years = new HashMap<>();
		for(int i=0;i<firstHundred.size();i++) {
			String year = firstHundred.get(i).getDateTime();
			String yearObtain = year.substring(0,year.indexOf("-"));
			years.put(yearObtain, yearObtain);
		}
		List<String> returnedYears = new ArrayList<>();
		years.forEach((k,v)->returnedYears.add(k));
		return returnedYears;
		
	}
	private Map<String, Integer> getMonthsAndDays(List<TrafficAccidents> accidents) {
	    Map<String, Integer> monthsAndDays = new HashMap<>();

	    for (TrafficAccidents accident : accidents) {
	        String dateTime = accident.getDateTime();
	        String datePart = dateTime.split(" ")[0]; 
	        String monthAndDay = datePart.substring(5);

	        monthsAndDays.put(monthAndDay, monthsAndDays.getOrDefault(monthAndDay, 0) + 1);
	    }

	    return monthsAndDays;
	}
	private Map<TrafficAccidents,String> getTrafficAccidentsByMunicipality(List<TrafficAccidents> firstHundred){
		
		Map<TrafficAccidents,String> municipalityAndTrafficAccidents = new HashMap<>();
		
		for(int i=0;i<firstHundred.size();i++) {
			for(int j=i+1;j<firstHundred.size();j++) {
				if(firstHundred.get(i).getMunicipality().equals(firstHundred.get(j).getMunicipality())) {
					
					municipalityAndTrafficAccidents.put(firstHundred.get(i), firstHundred.get(i).getMunicipality());
				}
				
				
			}
			
			
		}
		return municipalityAndTrafficAccidents;
		
	}
	
	//private String mainReasonDetection(List<TrafficAccidents> trafficAccidents) {
	//	Map<TrafficAccidents,String> mainReasonDefinition = new HashMap<>();
	//  for(int i=0;i<trafficAccidents.size();i++) {
	//	  if(trafficAccidents.get(i).get)
	 //}
	//}
	
	private List<String> getRoadSurfaceConditions(List<TrafficAccidents> retrievedList){
		Map<String,String> surfaceConditionMap = new HashMap<>();
		List<String> roadSurfaceTypes = new ArrayList<>();
		for(int i=0;i<retrievedList.size();i++) {
			surfaceConditionMap.put(retrievedList.get(i).getRoadSurfaceCondition(), retrievedList.get(i).getRoadSurfaceCondition());
		}
		surfaceConditionMap.forEach((k,v)->roadSurfaceTypes.add(k));
		return roadSurfaceTypes;
	}
	
	private int getDrunkOffenders(List<TrafficAccidents> retrievedList) {
		int counter=0;
		for(int i=0;i<retrievedList.size();i++) {
			if(retrievedList.get(i).getDrunkOffenders().equals("Taip")) {
				counter++;
			}
		}
		return counter;
	}
	private int getDrugImpairedOffenders(List<TrafficAccidents> retrievedList) {
		int counter=0;
		for(int i=0;i<retrievedList.size();i++) {
			if(retrievedList.get(i).getIntoxicatedOffenders().equals("Taip")) {
				counter++;
			}
		}
		return counter;
	}
	
	private int getDriverLicenceCount(List<TrafficAccidents> retrievedList) {
		int counter=0;
		for(TrafficAccidents accident: retrievedList) {
			for(TrafficParticipants participant : accident.getTrafficParticipants()) {
				if(!"Atitinka".equals(participant.getDriverQualification())) {
					counter++;
				}
			}
		}
		return counter;
	}
	
	
	
	
}