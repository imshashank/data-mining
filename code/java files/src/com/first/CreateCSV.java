package com.first;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.List;

public class CreateCSV {
	private static final String COLUMN_SEPARATER = ", ";
	public static boolean createCSVFile (List<Article> articlesList) {
		String newId;
//		List<String> topicsList;
//		List<String> placesList;
		String dateArticle;
		String titleArticle;
//		List<String> tokensOfBody;
		String body;
		File csvFile = new File("files", "pre_processing.csv");
		if (csvFile.exists()){
			System.out.println("The csv file already existed");
		}
		try {
			PrintWriter writer = new PrintWriter(csvFile);
			writer.print("newId");
			writer.print(COLUMN_SEPARATER);
			writer.print("TITLE");
			writer.print(COLUMN_SEPARATER);
			writer.print("DATE");
			writer.print(COLUMN_SEPARATER);
			writer.print("TOPICS");
			writer.print(COLUMN_SEPARATER);
			writer.print("PLACES");
			writer.print(COLUMN_SEPARATER);
			writer.print("BODY");
			writer.print("\n");
			
			for (Article article : articlesList){
				newId = article.getNewId();
				if (newId == null){
					newId = " ";
				}
				writer.print(newId);
				writer.print(COLUMN_SEPARATER);
				titleArticle = article.getTitleArticle();
				if (titleArticle == null) {
					titleArticle = " ";
				}
				writer.print(titleArticle);
				writer.print(COLUMN_SEPARATER);
				dateArticle = article.getDateArticle();
				if (dateArticle == null){
					dateArticle = "";
				}
				writer.print(article.getDateArticle());
				writer.print(COLUMN_SEPARATER);
				List<String> topics = article.getTopicsList();
				if (topics == null || topics.size() == 0) {
					writer.print("");
				} else {
					StringBuilder topicString = new StringBuilder();
					for (String topic : topics) {
						topicString.append(" ");
						topicString.append(topic);												
					}
					writer.print(topicString.substring(2));
				}
				writer.print(COLUMN_SEPARATER);
				List<String> places = article.getPlacesList();
				if (places == null || places.size() == 0) {
					writer.print("");
				} else {
					StringBuilder placesString = new StringBuilder();
					for (String place : places) {
						placesString.append(" ");
						placesString.append(place);												
					}
					writer.print(placesString.substring(2));
				}
				writer.print(COLUMN_SEPARATER);
				body = article.getBody();
				if (body == null){
					body = "";
				}
				writer.print(body);
				writer.print("\n");
			}
			writer.flush();
			writer.close();			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return false;
		}
		return true;
	}
}
