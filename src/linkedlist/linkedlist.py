import os.path
from flask import *

import models, config

app = Flask(__name__)
app.config.from_object(config)

def base_js():
	return ["https://code.jquery.com/jquery.js", url_for("static", filename="js/bootstrap.min.js")]

def base_css():
	return [url_for("static", filename="css/bootstrap.min.css")]

@app.route("/")
def index():
	return render_template("index.html", base_js=base_js(), base_css=base_css())

def run():
	if not os.path.isfile(config.DATABASE):
		models.create_tables()
	app.run()
