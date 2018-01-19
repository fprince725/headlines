import feedparser
import requests
import urllib
from datetime import datetime, timedelta
from flask import Flask
from flask import render_template 
from flask import request
from flask import make_response

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
		'cnn': 'http://rss.cnn.com/rss/edition.rss',
		'fox': 'http://feeds.foxnews.com/foxnews/latest',
		'iol': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'cnn',
		'city':'London,UK',
		'currency_from':'GBP',
		'currency_to':'USD'}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=5f877c391d82ae4903335178223ec8fa"

CURRENCY_URL = "https://api.openexchangerates.org/latest.json?app_id=6af38eb85058490b8501f4493d128ad3"

@app.route("/")
def home():

	publication = request.args.get("publication")
	if not publication:
		publication = request.cookies.get("publication")
		if not publication:
			publication = DEFAULTS['publication']
	articles = get_news(publication)

	city = request.args.get('city')
	if not city:
		city = DEFAULTS['city']
	weather = get_weather(city)

	currency_from = request.args.get('currency_from')
	if not currency_from:
		currency_from = DEFAULTS['currency_from']

	currency_to = request.args.get('currency_to')
	if not currency_to:
		currency_to = DEFAULTS['currency_to']
	currencies = None
	rate = None
	currencies, rate = get_rate(currency_from, currency_to)

	response = make_response(render_template("home.html",  publication=publication.upper(), articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies)))

	expires = datetime.now() + timedelta(days=365)
	response.set_cookie(publication, "publication", expires=expires)

	return response


def get_weather(query):
	query = urllib.quote(query)
	url = WEATHER_URL.format(query)
	parsed = requests.get(url).json()
	weather = None
	if parsed["weather"]:
		weather = {"description":parsed["weather"][0]["description"], "temperature":parsed["main"]["temp"], "city":parsed["name"], "country":parsed["sys"]["country"]}

	return weather

def get_rate(frm, to):
	parsed = requests.get(CURRENCY_URL).json()
	currencies = parsed["rates"]

	frm_rate =  None
	to_rate =  None
	frm_rate=parsed["rates"][frm]
	to_rate=parsed["rates"][to]
	return currencies, to_rate/frm_rate
		
def get_news(query):

	if not query or query.lower() not in RSS_FEEDS:
		publication = DEFAULTS['publication']
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])

	return feed['entries']

if __name__ == '__main__':
	app.run()
