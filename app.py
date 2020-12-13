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

from models import User, Performer, Customer, UserSchema, PerformerSchema, CustomerSchema, Job, JobSchema, Transaction, TransactionSchema

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
    return jsonify(performers_output)


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

    addedjob = Job(id=id, customer_id=customer_id, performer_id=performer_id, hours_booked=hours_booked,
                   start_time=start_time, date=date, address=address, price_per_hour=price_per_hour)
    db.session.add(addedjob)
    db.session.commit()

    job_schema = JobSchema()
    output = job_schema.dump(addedjob).data
    return jsonify(output)


@app.route('/performer/my_jobs/', methods=["GET", "POST"])
def list_jobs_performer():
    user_jobs = Job.query.all()
    # user_jobs = Job.query.filter_by(performer_id = request.json.get('performer_id'))
    job_schema = JobSchema(many=True)
    job_output = job_schema.dump(user_jobs).data
    return jsonify({'your jobs are': job_output})


@app.route('/customer/my_jobs/', methods=["GET", "POST"])
def list_jobs_customer():
    user_jobs = Job.query.all()
    # user_jobs = Job.query.filter_by(customer_id = request.json.get('customer_id'))
    #still need to figure out how the filter works
    job_schema = JobSchema(many=True)
    job_output = job_schema.dump(user_jobs).data
    return jsonify({'your jobs are': job_output})


@app.route('/delete_job/', methods=["POST"])
def delete_job():
    id = request.json.get('id')
    job = Job.query.filter_by(id=id)
    db.session.delete(job)
    db.session.commit()
    return "Job was deleted!"


@app.route('/update_job/', methods=["POST"])
def update_job():
    id = request.json.get('id')
    type = request.json.get('type')
    value = request.json.get('value')
    job = Job.query.filter_by(id=id)
    setattr(job, type, value)
    db.session.commit()






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
    user_transactions = Transaction.query.all()
    # user_transactions = Transaction.query.filter_by(performer_id = request.json.get('performer_id'))
    transaction_schema = TransactionSchema(many=True)
    transaction_output = transaction_schema.dump(user_transactions).data
    return jsonify({'your transactions are': transaction_output})


@app.route('/customer/my_jobs/', methods=["GET", "POST"])
def list_transactions_customer():
    user_transactions = Transaction.query.all()
    # user_transactions = Transaction.query.filter_by(customer_id = request.json.get('customer_id'))
    transaction_schema = TransactionSchema(many=True)
    transaction_output = transaction_schema.dump(user_transactions).data
    return jsonify({'your transactions are': transaction_output})


@app.route('/delete_transaction/', methods=["POST"])
def delete_transaction():
    id = request.json.get('id')
    transaction = Transaction.query.filter_by(id=id)
    db.session.delete(transaction)
    db.session.commit()
    return "The desired transaction was deleted!"


@app.route('/update_transaction/', methods=["POST"])
def update_job():
    id = request.json.get('id')
    type = request.json.get('type')
    value = request.json.get('value')
    transaction = Transaction.query.filter_by(id=id)
    setattr(transaction, type, value)
    transaction.updated_at = datetime.now()
    db.session.commit()
    return "The transaction was updated!"


if __name__ == '__main__':
    app.run()
