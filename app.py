import random
from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.getenv("DB_USER") + ':' + os.getenv("DB_PASSWORD") + '@' + os.getenv("DB_HOST") +'/'+ os.getenv("DB_NAME")

db.init_app(app)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        urlBase = request.form.get("urlInput")

        try:
            response = requests.get(urlBase)
        except:
            return render_template("index.html", urlShortenned = "")    
        
        if response.status_code == 200:
            return render_template("index.html", urlShortenned=generateUrl(urlBase, request.url))
        else:
            return render_template("index.html", urlShortenned = "")    
    return render_template("index.html", urlShortenned="")

def generateUrl(urlBase, url):
    return url+str(random.randrange(1000,9999))