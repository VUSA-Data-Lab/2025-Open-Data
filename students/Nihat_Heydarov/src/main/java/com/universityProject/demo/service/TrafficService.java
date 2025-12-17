package com.universityProject.demo.service;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.exc.StreamReadException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DatabindException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.universityProject.demo.model.TrafficAccidents;

@Service
public class TrafficService{
	
	public List<TrafficAccidents> getData() throws StreamReadException, DatabindException, IOException{
		String JsonPath ="C:/Users/Aydan/OneDrive/Desktop/ei_2024_12_31.json";
		File fl = new File(JsonPath);
		ObjectMapper objectMapper = new ObjectMapper();
		List<TrafficAccidents> objectList = objectMapper.readValue(fl, new TypeReference<List<TrafficAccidents>>() {});
		
		return objectList;
	}
}