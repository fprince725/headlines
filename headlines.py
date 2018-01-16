from flask import Flask

app = Flask(__name__)
@app.route("/headlines")
def index():
	return "Shell Flask app for headlines" 

if __name__ == '__main__':
	app.run()
