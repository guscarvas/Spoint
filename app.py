from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import Performer,Consumer
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY']='sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///website.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


@app.route('/',methods=['GET'])  # Root of your web platform
def home():
    return '<h1>Hello World!</h1>'




@app.route('/performers/', methods=['GET'])
def all_consumer():
    performers = Performer.query.all()
    return jsonify(performers)

@app.route('/consumer/', methods=['GET'])
def all_consumer():

    return jsonify()


if __name__ == '__main__':
    app.run()
