import feedparser
from flask import Flask

app = Flask(__name__)
@app.route("/headlines")
def getNews():
	return "No news is good news" 

if __name__ == '__main__':
	app.run()
