import os
import re
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from playhouse.shortcuts import model_to_dict
from werkzeug import exceptions
import datetime
import os

from peewee import MySQLDatabase, Model, CharField, TextField, DateTimeField, SqliteDatabase

load_dotenv()

app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")

    mydb = SqliteDatabase('file: memory?mode=memory&cache=shared', uri = True)
else:
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


@app.route('/timeline')
def timeline():
    posts = get_time_line_post()["timeline_posts"]

    return render_template('timeline.html', title="Timeline", url=os.getenv("URL"), posts=posts)


# DB Retrieval Endpoints
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    email_regex = re.compile(r"([A-Za-z0-9]+[--.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")

    key = ""
    try:
        key = "name"
        name = request.form[key]
        if len(name) == 0:
            raise exceptions.BadRequestKeyError(key)

        key = "email"
        email = request.form[key]
        is_email_valid = re.fullmatch(email_regex, email)
        if len(email) == 0 or not is_email_valid:
            raise exceptions.BadRequestKeyError(key)

        key = "content"
        content = request.form[key]
        if len(content) == 0:
            raise exceptions.BadRequestKeyError(key)

    except exceptions.BadRequestKeyError:

        return f"Invalid {key}", 400

    time_line_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(time_line_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route('/api/timeline_post', methods=['DELETE'])
def delete_post():
    post = TimelinePost.get(TimelinePost.id == request.form['id'])
    post.delete_instance()

    return "DELETE successful"
