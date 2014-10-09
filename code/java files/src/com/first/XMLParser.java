package com.first;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

public class XMLParser extends DefaultHandler{
	private List<Article> articleListInFile = null;
	private Article article;

	private boolean reuters = false;
	private boolean date = false;
	private boolean topics = false;
	private boolean places = false;
	private boolean title = false;
	private boolean body = false;

	@Override
	public void startElement(String uri, String localName, String qName,
			Attributes attributes) throws SAXException {
		super.startElement(uri, localName, qName, attributes);
		if (qName.equalsIgnoreCase("REUTERS")) {
			article = new Article();
			article.setNewId(attributes.getValue("NEWID"));
			reuters = true;
			if (articleListInFile == null) {
				articleListInFile = new ArrayList<Article>();
			}
		} else if (qName.equalsIgnoreCase("DATE")) {
			date = true;
		} else if (qName.equalsIgnoreCase("TOPICS")) {
			topics = true;
		} else if (qName.equalsIgnoreCase("PLACES")) {
			places = true;
		} else if (qName.equalsIgnoreCase("TITLE")) {
			title = true;
		} else if (qName.equalsIgnoreCase("BODY")) {
			body = true;
		}
	}

	@Override
	public void endElement(String uri, String localName, String qName)
			throws SAXException {
		super.endElement(uri, localName, qName);
		if (qName.equalsIgnoreCase("REUTERS")) {
			articleListInFile.add(article);
			reuters = false;
			article = null;
		} 
		// the reason I am toggling the status of element here and not in characters method is that for some elements
		// the characters method may be called multiple times (when the content is multi-line)
		else if (qName.equalsIgnoreCase("TOPICS")) {
			topics = false;
		} else if (qName.equalsIgnoreCase("PLACES")) {
			places = false;
		} else if (qName.equalsIgnoreCase("TITLE")) {
			title = false;
		} else if (qName.equalsIgnoreCase("BODY")) {
			body = false;
		}
	}

	@Override
	public void characters(char[] ch, int start, int length)
			throws SAXException {
		super.characters(ch, start, length);
		if (date) {
			article.setDateArticle(new String(ch, start, length));
			date = false;
		} else if (topics){
			List<String> topicList = article.getTopicsList();
			if (topicList == null) {
				topicList = new ArrayList<String>();
			}
			topicList.add(new String(ch, start, length));
			article.setTopicsList(topicList);
		} else if (places){
			List<String> placesList = article.getPlacesList();
			if (placesList == null) {
				placesList = new ArrayList<String>();
			}
			placesList.add(new String(ch, start, length));
			article.setPlacesList(placesList);
		} else if (title) {
			String titleArticle = article.getTitleArticle();
			if (titleArticle == null){
				titleArticle = new String();
			}
			titleArticle += new String(ch, start, length);
			article.setTitleArticle(titleArticle);
//			System.out.println("Title: " + article.getTitleArticle());
		} else if (body){
//			List<String> tokenList = article.getTokensOfBody();
//			if (tokenList == null) {
//				tokenList = new ArrayList<String>();
//			}
////			placesList.add(new String(ch, start, length));
//			String bodyLine = new String (ch, start, length);
//			tokenList.addAll(tokenize(bodyLine));
//			article.setTokensOfBody(tokenList);
			String bodyLine = article.getBody();
			if (bodyLine == null) {
				bodyLine = new String();
			}
			bodyLine += new String (ch, start, length);
			bodyLine = bodyLine.replaceAll("[,\\n\\t\'\";:!@#\\$%\\^&\\*\\(\\)\\{\\}\\[\\]\\\\\\|\\.\\?\\~]", " ");  // \n \t ' \" ; : !@#$%^&*() {} [] \ | . ?~
			article.setBody(bodyLine);
		}
	}

	public List<Article> getArticleListInFile() {
		return articleListInFile;
	}

	private List<String> tokenize (String line) {
//		System.out.println("Entering tokenize method");
		String[] tokens = line.split(" ");
		if (tokens != null) {
			return Arrays.asList(tokens);
		} else {
			System.out.println("The body line had 0 tokens!");
		}
		return null;
	}
}
