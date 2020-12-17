from datetime import datetime

from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

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

#<<<<<<< HEAD
from models import User, Performer, Customer, UserSchema, PerformerSchema, CustomerSchema, Job, JobSchema, Message, MessageSchema, Transaction, TransactionSchema


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
        password_hash = bcrypt.generate_password_hash(request.json.get('password')).encode('utf-8')
        role = request.json.get('role')
        name = request.json.get('name')
        fiscal_code = request.json.get('fiscal_code')
        address = request.json.get('address')
        birthday = request.json.get('birthday')

        newuser = User(email=email, password=password_hash, role=role)
        db.session.add(newuser)
        db.session.commit()

        if role == 'Performer':

            category = request.json.get('category')
            genre = request.json.get('genre')
            cost_per_hour = request.json.get('cost_per_hour')
            newperformer = Performer(email=email, user=newuser, name=name, category=category, genre=genre, birthday=birthday,
                                     cost_per_hour=cost_per_hour,fiscal_code=fiscal_code, address=address)
            db.session.add(newperformer)
        if role == 'Customer':
            newcustomer = Customer(email=email, user=newuser, name=name, birthday=birthday,
                                   fiscal_code=fiscal_code, address=address)
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
    elif request.method == 'PUT':
        performer_query.update(request.json)
    elif request.method == 'DEL':
        performer_output = performer_schema.dump(performer_query).data
        performer_query.delete()
        db.session.commit()
    return jsonify(performer_output)

@app.route('/search/', methods=['GET'])
def search():
    category = request.json.get('category')
    genre = request.json.get('genre')
    cost_minimum = request.json.get('cost_minimum')
    cost_max = request.json.get('cost_max')
    city = request.json.get('city')
    performers_query = Performer.query.filter_by(category=category, genre=genre, city=city).filter(cost_minimum < Performer.cost_per_hour < cost_max).all()
    performer_schema = PerformerSchema(many=True)
    performers_output = performer_schema.dump(performers_query).data
    return jsonify(performers_output)


@app.route('/consumer/', methods=['GET'])
def consumers():
    customers = Customer.query.all()
    customers_query = Customer.query.all()
    customer_schema = CustomerSchema(many=True)
    performers_output = customer_schema.dump(customers_query).data
    return jsonify(performers_output)


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


#HERE IS THE JOB CRUD
@app.route('/create_job/', methods=["POST"])
def create_job():
    customer_id = request.json.get('customer_id')
    performer_id = request.json.get('performer_id')
    hours_booked = request.json.get('hours_booked')
    start_time = request.json.get('start_time')
    date = request.json.get('date')
    address = request.json.get('address')
    price_per_hour = request.json.get('price_per_hour')
    # id = 2
    # customer_id = 1
    # performer_id = 1
    # hours_booked = 5.0
    # start_time = datetime.now()
    # date = datetime.now()
    # address = "Arena Corinthians"
    # price_per_hour = 85.0

    addedjob = Job(customer_id=customer_id, performer_id=performer_id, hours_booked=hours_booked,
                   start_time=start_time, date=date, address=address, price_per_hour=price_per_hour)
    db.session.add(addedjob)
    db.session.commit()

    job_schema = JobSchema()
    output = job_schema.dump(addedjob).data
    return jsonify(output)


@app.route('/performer/my_jobs/', methods=["GET", "POST"])
def list_jobs_performer():
    #user_jobs = Job.query.all()
    user_jobs = Job.query.get(request.json.get('performer_id'))
    job_schema = JobSchema(many=True)
    job_output = job_schema.dump(user_jobs).data
    return jsonify({'your jobs are': job_output})


@app.route('/customer/my_jobs/', methods=["GET", "POST"])
def list_jobs_customer():
    #user_jobs = Job.query.all()
    user_jobs = Job.query.get(request.json.get('customer_id'))
    #still need to figure out how the filter works
    job_schema = JobSchema(many=True)
    job_output = job_schema.dump(user_jobs).data
    return jsonify({'your jobs are': job_output})

@app.route('/delete_job/', methods=["POST"])
def delete_job():
    id = request.json.get('id')
    job = Job.query.get(id)
    db.session.delete(job)
    db.session.commit()
    return "Job was deleted!"

@app.route('/update_job/', methods=["POST"])
def update_job():
    id = request.json.get('id')
    type = request.json.get('type')
    value = request.json.get('value')
    job = Job.query.get(id)
    setattr(job, type, value)
    db.session.commit()

#front end sends job_id, by requesting jobs from user
# get request asking for information (no changes)
# Post request; creating something
# Del request: Deleting in database

@app.route('/show_job_messages/', methods=['GET'])
def show_job_messages():
    job_id = request.json.get('job_id')
    messages = Message.query.filter_by(job_id=job_id)
    messages_schema = MessageSchema(many=True)      # initialize message schema, receives list of object (many=true)
    messages_output = messages_schema.dump(messages).data  #Schema is an instruction for Marshmallow
    return jsonify(messages_output)

@app.route('/create_message/', methods=['POST'])
def create_message():
    customer_id = request.json.get('customer_id')
    performer_id = request.json.get('performer_id')
    job_id = request.json.get('job_id')
    content = request.json.get('content')
    sender = request.json.get('sender')
    added_message = Message(customer_id=customer_id, performer_id=performer_id, job_id=job_id, content=content, sender=sender)
    db.session.add(added_message)
    db.session.commit()
    messages_schema = MessageSchema()
    output = messages_schema.dump(added_message).data
    return jsonify(output)

    #create new messages
    #shows all the messages



































#showcustomer/chats

#send message

#show_a_conversation

#delete chat



#HERE IS THE TRANSACTION CRUD
@app.route('/transaction/', methods=["POST"])
def create_transaction():
    value = request.json.get('value')
    code = request.json.get('code')
    new_transaction = Transaction(value=value, code=code)
    db.session.add(new_transaction)
    db.session.commit()

    transaction_schema = TransactionSchema()
    output = transaction_schema.dump(new_transaction).data
    return jsonify(output)


@app.route('/performer/my_jobs/', methods=["GET", "POST"])
def list_transactions_performer():
    #user_transactions = Transaction.query.all()
    user_transactions = Transaction.query.get(request.json.get('performer_id'))
    transaction_schema = TransactionSchema(many=True)
    transaction_output = transaction_schema.dump(user_transactions).data
    return jsonify({'your transactions are': transaction_output})


@app.route('/customer/my_jobs/', methods=["GET", "POST"])
def list_transactions_customer():
    #user_transactions = Transaction.query.all()
    user_transactions = Transaction.query.get(request.json.get('customer_id'))
    transaction_schema = TransactionSchema(many=True)
    transaction_output = transaction_schema.dump(user_transactions).data
    return jsonify({'your transactions are': transaction_output})


@app.route('/delete_transaction/', methods=["POST"])
def delete_transaction():
    id = request.json.get('id')
    transaction = Transaction.query.get(id)
    db.session.delete(transaction)
    db.session.commit()
    return "The desired transaction was deleted!"


@app.route('/update_transaction/', methods=["POST"])
def update_job():
    id = request.json.get('id')
    type = request.json.get('type')
    value = request.json.get('value')
    transaction = Transaction.query.get(id)
    setattr(transaction, type, value)
    transaction.updated_at = datetime.now()
    db.session.commit()
    return "The transaction was updated!"


if __name__ == '__main__':
    app.run()
