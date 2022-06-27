import os
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv

from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

import json

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                     user=os.getenv("MYSQL_USER"),
                     password=os.getenv("MYSQL_PASSWORD"),
                     host=os.getenv("MYSQL_HOST"),
                     port=3306)


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])


@app.route('/')
def index():
    return render_template('index.html', title="About Me", url=os.getenv("URL"))


@app.route('/experience')
def experience():
    data_path = os.path.join(app.static_folder, 'data', 'oscar_experience.json')
    job_list = json.load(open(data_path))

    return render_template('work_experience.html', title="Experience", url=os.getenv("URL"), job_list=job_list)


@app.route('/hobbies')
def hobbies():
    data_path = os.path.join(app.static_folder, 'data', 'oscar_hobbies.json')
    hobby_list = json.load(open(data_path))

    return render_template('hobbies.html', title="Hobbies", hobby_list=hobby_list, url=os.getenv("URL"))


@app.route('/education')
def education():
    return render_template('education.html', title="Education", url=os.getenv("URL"))


@app.route('/places')
def places():
    countries = ["Mexico", "United States", "Canada", "Germany", "Italy", "France", "Spain"]
    countries.sort()
    return render_template('places.html', title="Places Visited", url=os.getenv("URL"), countries=countries)


@app.route('/projects')
def projects():
    return render_template('projects_and_skills.html', title="Projects", url=os.getenv("URL"))


# Retrieval Endpoints
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['name']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
