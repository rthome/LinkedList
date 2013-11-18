import os.path
from flask import *

import models, config

app = Flask(__name__)
app.config.from_object(config)

@app.before_request
def init_base_args():
	g.base_template_args = {}
	g.base_template_args.update({"js": ["https://code.jquery.com/jquery.js", url_for("static", filename="js/bootstrap.min.js")], \
								 "css": [url_for("static", filename="css/bootstrap.min.css")]})

@app.route("/")
def index():
	return render_template("index.html", base=g.base_template_args)

@app.route("/login")
def login():
	return render_template("login.html", base=g.base_template_args)

def run():
	if not os.path.isfile(config.DATABASE):
		models.create_tables()
	app.run()
