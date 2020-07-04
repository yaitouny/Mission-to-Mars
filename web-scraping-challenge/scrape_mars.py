from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	return Browser('chrome', **executable_path, headless=False)

mars_dictionnary = {}

def scrape():
	# Initialize browser
	browser = init_browser()

	# Visit Nasa news using Splinter
	url = "https://mars.nasa.gov/news/"
	browser.visit(url)

	html = browser.html
	news_soup = BeautifulSoup(html, 'lxml')
	
	titles = news_soup.find_all('div', class_="content_title")
	p = news_soup.find_all('div', class_="article_teaser_body")
	first_title = ""
	for title in titles:
			if title.a:
					first_title = title
					break
	news_title = first_title.a.text.strip()
	news_p = p[0].text.strip()

	# Visit the url for JPL Featured Space Image
	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)
	html = browser.html
	image_soup = BeautifulSoup(html, "lxml")

	image = image_soup.find_all(class_="carousel_item")
	featured_image_url = 'https://www.jpl.nasa.gov' + image[0]["style"].split(" ")[1].split("'")[1]
	

	# Visit the Mars Weather twitter 
	url = "https://twitter.com/marswxreport?lang=en"
	browser.visit(url)
	html = browser.html
	weather_soup = BeautifulSoup(html, 'lxml')
	mars_weather = weather_soup.find_all("span")
	mars_weather_tweet = ""
	for tweet in mars_weather:
			if tweet.text:
					if "InSight sol" in tweet.text:
											mars_weather_tweet = tweet.text
											break


	# Visit the Mars Facts webpage
	url = "https://space-facts.com/mars/"
	browser.visit(url)
	html = browser.html
	fact_soup = BeautifulSoup(html, 'lxml')
	table = pd.read_html(url)
	df = table[0]
	df.columns = ['Attribute', 'Values']
	fact_table = df.to_html("Mars_Profile.html")

	# Visit the USGS Astrogeology site
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url)
	html = browser.html
	hemisphere_soup = BeautifulSoup(html, 'lxml')
	items = hemisphere_soup.find_all('div', class_='item')

	hemisphere_image_urls = []
	for item in items:
			title = item.find('h3').text
			link = item.find('a', class_="itemLink")['href']
			hemisphere_link = "https://astrogeology.usgs.gov" + link
			browser.visit(hemisphere_link)
			hemisphere_html = browser.html
			new_soup = BeautifulSoup(hemisphere_html, 'lxml')
			image = new_soup.find('img', class_="wide-image")['src']
			img_url = "https://astrogeology.usgs.gov"+ image
			hemisphere_image_urls.append({"title": title, "image_url":img_url})


	# close the browser
	browser.quit()

	scraped_dict = {
		"News Title": news_title,
		"News Paragraph": news_p,
		"Featured_image_url": featured_image_url,
		"Mars Weather": mars_weather_tweet,
		"Mars Facts": fact_table,
		"Hemisphere URL": hemisphere_image_urls
	}

	return scraped_dict


if __name__ == "__main__":
		print(scrape())