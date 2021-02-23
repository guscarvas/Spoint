from datetime import datetime

from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_cors import CORS

import os
import sqlite3

# steven

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sssdhgclshfsh;shd;jshjhsjhjhsjldchljk'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

from models import User, Performer, Customer, UserSchema, PerformerSchema, CustomerSchema, Job, JobSchema, Message, MessageSchema, Transaction, TransactionSchema, Report, ReportSchema


db.create_all()
db.session.commit()


@app.route('/', methods=['GET'])  # Root of your web platform
def home():
    return '<h1>Hello World!</h1>'


#############
#### USERS

@app.route('/user/', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        print(request.json)

        email = request.json.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            return "This email is already registered"
        password_hash = bcrypt.generate_password_hash(request.json.get('password')).encode('utf-8')
        role = request.json.get('role')
        name = request.json.get('name')
        fiscal_code = request.json.get('fiscal_code')
        address = request.json.get('address')
        search_city = request.json.get('search_city')
        birthday = request.json.get('birthday')
        birthday = datetime.strptime(birthday, '%d-%m-%Y')
        profile_pic_url = "ABC"
        if request.json.get('profile_pic_url'):
            profile_pic_url = request.json.get('profile_pic_url')

        newuser = User(email=email, password=password_hash, role=role)
        db.session.add(newuser)
        db.session.commit()

        if role == 'Performer':

            category = request.json.get('category')
            genre = request.json.get('genre')
            cost_per_hour = request.json.get('cost_per_hour')
            newperformer = Performer(email=email, user=newuser, name=name, category=category, genre=genre, birthday=birthday,
                                     cost_per_hour=cost_per_hour,fiscal_code=fiscal_code, address=address, search_city=search_city,
                                     profile_pic_url=profile_pic_url)
            db.session.add(newperformer)
            performer_schema = PerformerSchema()
            output = performer_schema.dump(newperformer).data
        if role == 'Customer':
            newcustomer = Customer(email=email, user=newuser, name=name, birthday=birthday,
                                   fiscal_code=fiscal_code, address=address, profile_pic_url=profile_pic_url)
            db.session.add(newcustomer)
            customer_schema = CustomerSchema()
            output = customer_schema.dump(newcustomer).data
        db.session.commit()
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
    elif request.method == 'PUT':
        performer_query.update(request.json)
        performer_output = performer_schema.dump(performer_query).data
    elif request.method == 'DEL':
        performer_output = performer_schema.dump(performer_query).data
        performer_query.delete()
        db.session.commit()
    return jsonify(performer_output)

@app.route('/search/', methods=['GET'])
def search():
    performers_query = Performer.query
    if request.json.get('city'):
        city = request.json.get('city')
        performers_query = performers_query.filter_by(search_city=city)
    if request.json.get('category'):
        category = request.json.get('category')
        performers_query = performers_query.filter_by(category=category)
    if request.json.get('genre'):
        genre = request.json.get('genre')
        performers_query.filter_by(genre=genre)
    if request.json.get('cost_minimum'):
        cost_minimum = request.json.get('cost_minimum')
        performers_query = performers_query.filter(Performer.cost_per_hour > cost_minimum)
    if request.json.get('cost_max'):
        cost_max = request.json.get('cost_max')
        performers_query.filter(Performer.cost_per_hour > cost_max)



    # category = request.json.get('category')
    # genre = request.json.get('genre')
    # cost_minimum = request.json.get('cost_minimum')
    # cost_max = request.json.get('cost_max')
    # performers_query = Performer.query.filter_by(category=category, genre=genre, search_city=city)
    # performers_query = performers_query.filter(Performer.cost_per_hour > cost_minimum).filter(Performer.cost_per_hour < cost_max).all()
    performer_schema = PerformerSchema(many=True)
    performers_output = performer_schema.dump(performers_query).data
    return jsonify({'performers': performers_output})



@app.route('/customer/', methods=['GET'])
def customers():
    customers_query = Customer.query.all()
    customer_schema = CustomerSchema(many=True)
    customers_output = customer_schema.dump(customers_query).data
    return jsonify(customers_output)


@app.route('/customer/<int:id_customer>', methods=['GET', 'PUT', 'DEL'])
def customer(id_customer):
    customer_query = Customer.query.get(id_customer)
    customer_schema = CustomerSchema()
    if request.method == 'GET':
        customer_output = customer_schema.dump(customer_query).data

    elif request.method == 'PUT':
        customer_query.update(request.json)
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


@app.route('/login/', methods=['GET'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user == None:
        return "Incorrect email"
    if bcrypt.check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["role"] = user.role
        if user.performer:
            performer_schema = PerformerSchema()
            output = performer_schema.dump(user.performer).data
            return jsonify(output)
        else:
            customer_schema = CustomerSchema()
            output = customer_schema.dump(user.customer).data
            return jsonify(output)

    else:
        return "Log in failed"


@app.route('/job/', methods=["POST"])
def create_job():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user == None:
        return "Incorrect email"

    if bcrypt.check_password_hash(user.password, password):
        if user.customer:
            customer_id = request.json.get('customer_id')
            customer_query = Customer.query.get(customer_id)
            performer_id = request.json.get('performer_id')
            performer_query = Performer.query.get(performer_id)

            title = request.json.get('title')
            start_time = request.json.get('start_time')
            start_time = datetime.strptime(start_time, '%Y-%m-%d, %H:%M')
            end_time = request.json.get('end_time')
            end_time = datetime.strptime(end_time, '%Y-%m-%d, %H:%M')

            address = request.json.get('address')
            price_per_hour = request.json.get('price_per_hour')


            addedjob = Job(customer=customer_query, performer=performer_query, performer_name=performer_query.name, customer_name=customer_query.name,
                           title=title, end_time=end_time,start_time=start_time, address=address, price_per_hour=price_per_hour)
            db.session.add(addedjob)
            db.session.commit()

            job_schema = JobSchema()
            output = job_schema.dump(addedjob).data
            return jsonify(output)


@app.route('/my_jobs/', methods=["GET"])
def list_jobs():

    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user == None:
        return "Incorrect email"

    if bcrypt.check_password_hash(user.password, password):
        if user.performer:
            user_jobs = Job.query.filter_by(performer=user.performer)
            job_schema = JobSchema(many=True)
            job_output = job_schema.dump(user_jobs).data
        else:
            user_jobs = Job.query.filter_by(customer=user.customer)
            job_schema = JobSchema(many=True)
            job_output = job_schema.dump(user_jobs).data
    else:
        return "Invalid credentials"

    return jsonify({'your jobs are': job_output})

@app.route('/delete_job/', methods=["POST"])
def delete_job():
    id = request.json.get('id')
    job = Job.query.get(id)
    db.session.delete(job)
    db.session.commit()
    return "Job was deleted!"

@app.route('/update_job/', methods=["PATCH"])
def update_job():

    job_id = request.json.get('job_id')
    status = request.json.get('status')

    job_query = Job.query.get(job_id)
    job_query.status = status

    db.session.commit()
    return "Updated"

if __name__ == '__main__':
    app.run()
