import random
from flask import Flask, redirect, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from sqlalchemy import func
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

@app.route('/<short>')
def redirectToUrl(short):
    shortened = Shortened.query.filter_by(short=short).first()
    try:
        return redirect(shortened.url)
    except:
        return render_template("index.html", urlShortenned = "") 


def generateUrl(urlBase, url):
    short=random.randrange(1000,9999)
    newUrl = Shortened(url=urlBase, short=short)
    db.session.add(newUrl)
    db.session.commit()
    return url+str(newUrl.short)

class Shortened(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   url = db.Column(db.String(200))
   short = db.Column(db.String(9))
   created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
