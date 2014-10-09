package com.first;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.apache.xml.utils.XMLChar;

public class FirstTry {

	public static void main(String[] args) {
		/*
		 * Implement a logging functinality
		 * Better way to read a file. Either we should have all text files in same location
		 * as the executable or we should be able to specify the folder path
		 */
		new FirstTry().tokenizeFiles();

	}
	public void tokenizeFiles() {
		File filesDir = new File("files");
		List<Article> allArticles = new ArrayList<Article>();
		XMLParser parser = null;
		System.out.println("filesDir.isDirectory(): " + filesDir.isDirectory());
		for (File currentFile : filesDir.listFiles()) {
			System.out.println("Reading filename: " + currentFile.getName());
			if (currentFile.getName().equalsIgnoreCase("lewis.dtd")) {
				continue;
			}
			cleanXML(currentFile);
			SAXParserFactory saxParserFactory = SAXParserFactory.newInstance();
			saxParserFactory.setValidating(false);
			saxParserFactory.setNamespaceAware(false);
			SAXParser saxParser = null;
			try {
				saxParser = saxParserFactory.newSAXParser();
				parser = new XMLParser();
				saxParser.parse(currentFile, parser);
				allArticles.addAll(parser.getArticleListInFile());
			} catch (Exception e) {
				e.printStackTrace();
			}

//			for (Article article : parser.getArticleListInFile()) {
////				System.out.println("Date: " + article.getDateArticle());
////				System.out.println("Topics: " + article.getTopicsList());
//				System.out.println("article.getNewId(): " + article.getNewId());
//				System.out.println("getTitleArticle(): " + article.getTitleArticle());
////				System.out.println("getPlacesList(): " + article.getPlacesList());
////				System.out.println("TokensOfBody(): " + article.getTokensOfBody());
//				System.out.println("body: " + article.getBody());
//			}			
		}
		CreateCSV.createCSVFile(allArticles);
	}

	private void cleanXML (File file) {
		System.out.println("Entering cleanXML");
		/*
		String line = "&#22;&#22;&#1;f0011&#31;reute";
		System.out.println("line: " + line);
		line = line.replaceAll("&#\\d+;", " ");
		System.out.println("new line: " + line);*/
		String line = null;
		StringBuilder stringBuilder = new StringBuilder();
		//adding a root element
		stringBuilder.append("<myroot>" + "\n");
		try {
			BufferedReader reader = new BufferedReader(new FileReader(file));
			while ( (line = reader.readLine()) != null) {
				
				//removing the DTD line
				if (line.contains("!DOCTYPE")) {
					continue;
				}				
				line = line.replaceAll("&#\\d+;", " ");
//				line = line.replaceAll("[\n\t\'\";:!@#$%^&]", " ");
//				line = line.replaceAll("[\n\t\'\"\;\:\!@#\$%\^&\*\(\){}\[\]\\\|\.\?\~]", " ");
				
				stringBuilder.append(line);
				stringBuilder.append("\n");
			}
			reader.close();
			//adding a root element
			stringBuilder.append("</myroot>");
			PrintWriter writer = new PrintWriter(file);
			writer.print(stringBuilder.toString());
			writer.flush();
			writer.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println("Exiting cleanXML");
		
		/*
		try {
			BufferedReader reader = new BufferedReader(new FileReader(file));
			String line = null;
			StringBuilder stringBuilder = new StringBuilder();
			String testStr = null;
			
			Pattern p = Pattern.compile("^&[\\d\\w#]+;$");
			
			 
			testStr = "<DATE>26-FEB-1987 15:01:01.79</DATE>";
			System.out.println("testStr: " + testStr);
//			System.out.println("replace: " + testStr.replaceAll("^&[\\d\\w#]+;$", " "));
			 Matcher m = p.matcher(testStr);
			 System.out.println(m.matches());
			
			testStr = "&#5;&#5;&#5;C T";
			System.out.println("testStr: " + testStr);
			 m = p.matcher(testStr);
			 System.out.println(m.matches());
			
			while ( (line = reader.readLine()) != null){
//				System.out.println("line: " + line);
				//				System.out.println("replace: " + line.replaceAll( "&([^;]+(?!(?:\\w|;)))", "&amp;$1" ));
				//				stringBuilder.append(line.replaceAll( "&([^;]+(?!(?:\\w|;)))", "&amp;$1" ));
				/*for (int i = 0; i < line.length(); i++) {
					char c = line.charAt(i);
					if (XMLChar.isValid(c)) {
						stringBuilder.append(c);
					}
				}
				stringBuilder.append("\n");
				

			}
			System.out.println("is valid: " + XMLChar.isValid('#'));
			reader.close();
			PrintWriter writer = new PrintWriter(file);
			writer.print(stringBuilder.toString());
			writer.flush();
			writer.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		System.out.println("Exiting cleanXML");
	}
*/
	}
}
