import flask 
import atexit
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,send_from_directory,send_file
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func
from webapps import youtube_api


#                           Flask
#################################################################
website = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')
website.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#website.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yagmurerva/Desktop/webserver.db'
db = SQLAlchemy(website)
downloadedfiles=[]
alerts=[]

@website.route('/')
def index():
    return render_template("mainpage.html")

@website.route('/home')
def home():
    return render_template("mainpage.html")
@website.route('/about')
def about():
    return render_template("about.html")

@website.route('/youtube',methods = ["GET","POST"])
def youtubeSearch():
    if request.method == 'POST':
        url = request.form['youtube-link']
        avaibleformats = youtube_api.search_video(url)
        url = url.split("=")[1]
        alldata= [avaibleformats,url,alerts]
        return render_template("select_page.html",alldata=alldata)
    else:
        return render_template("youtubepage.html")

@website.route('/download/<string:url>/<string:type>-<string:id>',methods = ["GET","POST"])
def youtubeDownload(url,type,id):
    if request.method == 'POST':
        return render_template("mainpage.html")
    else:
        file = youtube_api.download_source(url,type,id)
        downloadedfiles.append(file)
        return send_file(file,as_attachment=True)

def cleaner():
    import os
    for i in downloadedfiles:
        os.remove(i)
        
atexit.register(cleaner)

if __name__=="__main__":
    website.run(debug=True)
