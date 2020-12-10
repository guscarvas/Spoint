from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY']='sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from models import User, Performer, Customer

db.create_all()
db.session.commit()

@app.route('/',methods=['GET'])  # Root of your web platform
def home():
    return '<h1>Hello World!</h1>'



################# USERS

@app.route('/user/',methods=['GET','POST'])
def users():
    if request.method == 'POST':
        print(request.json)
        email = request.json.get('email')
        password_hash = bcrypt.generate_password_hash(request.json.get('password')).encode('utf-8')
        role = request.json.get('role')
        newuser = User(email=email, password=password_hash, role=role)
        db.session.add(newuser)
        db.session.commit()
        print(newuser.id)
        name = request.json.get('name')
        if role == 'Performer':
            newperformer = Performer(email=email, user_id=newuser.id, name=name)
            newuser.performer_id = newperformer.id
            db.session.add(newperformer)
        if role == 'Customer':
            newcustomer = Customer(email=email, user_id=newuser.id, name=name)
            newuser.customer_id = newcustomer.id
            db.session.add(newcustomer)
        db.session.commit()
        return jsonify(newuser)

@app.route('/performers/', methods=['GET'])
def performers():
    performers = Performer.query.all()
    return jsonify(performers)

@app.route('/consumers/', methods=['GET'])
def all_consumer():
    customers = Customer.query.all()
    return jsonify(customers)

@app.route('/restartdb/',methods=['GET'])
def restart():
    User.query.delete()
    Performer.query.delete()
    Customer.query.delete()

@app.route('/login/',methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if bcrypt.check_password_hash(user.password,password):
        print('logged in')
        session["user_id"] = user.id
        session["role"] = user.role
#         return logged user and info?

if __name__ == '__main__':
    app.run()
