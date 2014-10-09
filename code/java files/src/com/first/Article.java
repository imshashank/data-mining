package com.first;

import java.util.List;

public class Article {
	private String newId;
	private List<String> topicsList;
	private List<String> placesList;
	private String dateArticle;
	private String titleArticle;
	private List<String> tokensOfBody;
	private String body;
	public List<String> getTopicsList() {
		return topicsList;
	}
	public void setTopicsList(List<String> topicsList) {
		this.topicsList = topicsList;
	}
	public List<String> getPlacesList() {
		return placesList;
	}
	public void setPlacesList(List<String> placesList) {
		this.placesList = placesList;
	}
	public String getDateArticle() {
		return dateArticle;
	}
	public void setDateArticle(String dateArticle) {
		this.dateArticle = dateArticle;
	}
	public String getTitleArticle() {
		return titleArticle;
	}
	public void setTitleArticle(String titleArticle) {
		this.titleArticle = titleArticle;
	}
	public List<String> getTokensOfBody() {
		return tokensOfBody;
	}
	public void setTokensOfBody(List<String> tokensOfBody) {
		this.tokensOfBody = tokensOfBody;
	}
	public String getNewId() {
		return newId;
	}
	public void setNewId(String newId) {
		this.newId = newId;
	}
	public String getBody() {
		return body;
	}
	public void setBody(String body) {
		this.body = body;
	}
	
	
}
