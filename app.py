from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

from models import User, Performer, Customer, UserSchema, PerformerSchema, CustomerSchema

db.create_all()
db.session.commit()


@app.route('/', methods=['GET'])  # Root of your web platform
def home():
    return '<h1>Hello World!</h1>'


################# USERS

@app.route('/user/', methods=['GET', 'POST'])
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
            newperformer = Performer(email=email, user=newuser, name=name)
            db.session.add(newperformer)
        if role == 'Customer':
            newcustomer = Customer(email=email, user_id=newuser.id, name=name)
            newuser.customer_id = newcustomer.id
            db.session.add(newcustomer)
        db.session.commit()
        user_schema = UserSchema()
        output = user_schema.dump(newuser).data
        return jsonify(output)


@app.route('/performer/', methods=['GET'])
def performers():
    performers_query = Performer.query.all()
    performer_schema = PerformerSchema(many=True)
    performers_output = performer_schema.dump(performers_query).data
    return jsonify(performers_output)


@app.route('/performer/<int:id_performer>', methods=['GET', 'PUT', 'DEL'])
def performer(id_performer):
    performer_query = Performer.query.get(id_performer)
    performer_schema = PerformerSchema()
    if request.method == 'GET':
        performer_output = performer_schema.dump(performer_query).data
        print("passei no GET")
    elif request.method == 'PUT':
        pass
    elif request.method == 'DEL':
        performer_output = performer_schema.dump(performer_query).data
        performer_query.delete()
        db.session.commit()
    return jsonify(performer_output)


@app.route('/consumer/', methods=['GET'])
def consumers():
    customers = Customer.query.all()
    customers_query = Customer.query.all()
    customer_schema = CustomerSchema(many=True)
    performers_output = customer_schema.dump(customers_query).data
    return jsonify(customers_output)


@app.route('/customer/<int:id_customer>', methods=['GET', 'PUT', 'DEL'])
def customer(id_customer):
    customer_query = Customer.query.get(id_customer)
    customer_schema = CustomerSchema()
    if request.method == 'GET':
        customer_output = customer_schema.dump(customer_query).data

    elif request.method == 'PUT':
        pass
    elif request.method == 'DEL':
        customer_output = customer_schema.dump(customer_query).data
        customer_query.delete()
        db.session.commit()
    return jsonify(customer_output)


@app.route('/restartdb/', methods=['GET'])
def restart():
    User.query.delete()
    Performer.query.delete()
    Customer.query.delete()


@app.route('/login/', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if bcrypt.check_password_hash(user.password, password):
        print('logged in')
        session["user_id"] = user.id
        session["role"] = user.role


#         return logged user and info?

if __name__ == '__main__':
    app.run()

# from sqlathanor import FlaskBaseModel, initialize_flask_sqlathanor
# from flask import Flask, jsonify, request, session
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
#
# import os
# import sqlite3
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
#
# THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
# my_file = os.path.join(THIS_FOLDER, 'website.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = my_file
#
# db = SQLAlchemy(app, model_class=FlaskBaseModel)
# db = initialize_flask_sqlathanor(db)
# bcrypt = Bcrypt(app)
#
# from models import User, Performer, Customer
#
# db.create_all()
# db.session.commit()
#
# @app.route('/',methods=['GET'])  # Root of your web platform
# def home():
#     return '<h1>Hello World!</h1>'
#
#
#
# ################# USERS
#
# @app.route('/user/',methods=['GET','POST'])
# def users():
#     if request.method == 'POST':
#         print(request.json)
#         email = request.json.get('email')
#         password_hash = bcrypt.generate_password_hash(request.json.get('password')).encode('utf-8')
#         role = request.json.get('role')
#         newuser = User(email=email, password=password_hash, role=role)
#         db.session.add(newuser)
#         db.session.commit()
#         print(newuser.id)
#         name = request.json.get('name')
#         if role == 'Performer':
#             newperformer = Performer(email=email, user_id=newuser.id, name=name)
#             # newuser.performer_id = newperformer.id
#             db.session.add(newperformer)
#         if role == 'Customer':
#             newcustomer = Customer(email=email, user_id=newuser.id, name=name)
#             # newuser.customer_id = newcustomer.id
#             db.session.add(newcustomer)
#         db.session.commit()
#         return User.to_json(newuser)
#
# @app.route('/performers/', methods=['GET'])
# def performers():
#     performers = Performer.query.all()
#     return jsonify(performers)
#
# @app.route('/consumers/', methods=['GET'])
# def all_consumer():
#     customers = Customer.query.all()
#     return jsonify(customers)
#
# @app.route('/restartdb/',methods=['GET'])
# def restart():
#     User.query.delete()
#     Performer.query.delete()
#     Customer.query.delete()
#
# @app.route('/login/',methods=['POST'])
# def login():
#     email = request.json.get('email')
#     password = request.json.get('password')
#     user = User.query.filter_by(email=email).first()
#     if bcrypt.check_password_hash(user.password,password):
#         print('logged in')
#         session["user_id"] = user.id
#         session["role"] = user.role
# #         return logged user and info?
#
# if __name__ == '__main__':
#     app.run()
