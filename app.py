import random
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

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