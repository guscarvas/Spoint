from app import db, ma
from marshmallow_sqlalchemy import ModelSchema
import json


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    performer = db.relationship('Performer', uselist=False, backref="user")
    customer = db.relationship('Customer', uselist=False, backref="user")

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    # child = db.relationship('Child', uselist=False, backref="parent")
    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role

class Performer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    jobs = db.relationship('Job', backref='performer')

    name = db.Column(db.String(50), nullable=False)
    cost_per_hour = db.Column(db.Float, nullable=False, default=100)
    genre = db.Column(db.String(120), nullable=False, default="Rock")
    category = db.Column(db.String(120), nullable=False, default="Band")
    profile_pic_url = db.Column(db.String(100), nullable=True)
    birthday = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Float, nullable=False, default=0)
    search_city = db.Column(db.String(30), nullable=False)
    fiscal_code = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    money = db.Column(db.Float, nullable=False, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    # parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    jobs = db.relationship('Job', backref='customer')

    # user = db.relationship("User", back_populates="customer")

    name = db.Column(db.String(50), nullable=False)
    profile_pic_url = db.Column(db.String(50), nullable=True)
    birthday = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Float, nullable=False, default=0)
    fiscal_code = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    performer_id = db.Column(db.Integer, db.ForeignKey('performer.id'))

    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    performer_score = db.Column(db.Float, nullable=False, default=0)

    # customer_score =

    price_per_hour = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    status = db.Column(db.String(20), nullable=False, default="Pending")
    # Status will be one of these options: 'Pending', 'Accepted', 'Finished' and maybe 'Reviewed'? Don't know yet


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(20), nullable=False)

    # performer = db.relationship('Performer', uselist=False, backref="user")
    # customer = db.relationship('Customer', lazy=True, uselist=False, back_populates="user")

    # def __init__(self, email, password, role):
    #     self.email = email
    #     self.password = password
    #     self.role = role



class UserSchema(ModelSchema):
    class Meta:
        model = User
        sql_session = db.session


# class Performer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#
#     # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     # user = db.relationship("User", back_populates="performer")
#
#     name = db.Column(db.String(50), nullable=False)
#     cost_per_hour = db.Column(db.Float, nullable=False, default=100)
#     genre = db.Column(db.String(120), nullable=False, default="Rock")
#     category = db.Column(db.String(120), nullable=False, default="Band")
#     profile_pic_url = db.Column(db.String(100), nullable=True)
#     birthday = db.Column(db.DateTime, nullable=False)
#     score = db.Column(db.Float, nullable=False, default=0)
#     search_city = db.Column(db.String(30), nullable=False)
#     fiscal_code = db.Column(db.String(20), nullable=False)
#     address = db.Column(db.String(100), nullable=False)
#     money = db.Column(db.Float, nullable=False, default=0)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    #
    # messages = db.relationship('Message', backref='customer', lazy=True)
    # jobs = db.relationship('Job', backref='performer', lazy=True)

    # def update(self,jsonInfo):
    #     if jsonInfo.get('email'):
    #         user = User.query.get(self.user_id)
    #         user.email = jsonInfo.get('email')
    #     for key, value in jsonInfo.iteritems():
    #         setattr(self, key, value)
    #     db.session.commit()



class PerformerSchema(ModelSchema):
    class Meta:
        model = Performer
        sql_session = db.session


# class Customer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     #
#     # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     # user = db.relationship("User", back_populates="customer")
#
#     name = db.Column(db.String(50), nullable=False)
#     profile_pic_url = db.Column(db.String(50), nullable=True)
#     birthday = db.Column(db.DateTime, nullable=False)
#     score = db.Column(db.Float, nullable=False, default=0)
#     fiscal_code = db.Column(db.String(20), nullable=False)
#     address = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # jobs = db.relationship('Job', backref='customer', lazy=True)
    # messages = db.relationship('Message', backref='customer', lazy=True)
    #
    # def update(self,jsonInfo):
    #     if jsonInfo.get('email'):
    #         user = User.query.get(self.user_id)
    #         user.email = jsonInfo.get('email')
    #     for key, value in jsonInfo.iteritems():
    #         setattr(self, key, value)
    #     db.session.commit()

class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer
        sql_session = db.session

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # performer_id = db.Column(db.Integer, db.ForeignKey('performer.id', nullable=False))
    # job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    sender = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(200), nullable=False)

class MessageSchema(ModelSchema):
    class Meta:
        model = Message
        sql_session = db.session
#
# class Job(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     #
#     # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False )
#     # performer_id = db.Column(db.Integer, db.ForeignKey('performer.id'), nullable=False)
#
#     # messages = db.relationship('Message', backref='job', lazy=True)
#
#     hours_booked = db.Column(db.Float, nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False)
#     performer_score = db.Column(db.Float, nullable=False, default=0)
#     date = db.Column(db.DateTime, nullable=False)
#     # customer_score =
#
#     price_per_hour = db.Column(db.Float, nullable=False)
#     address = db.Column(db.String(80), nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
#
#     status = db.Column(db.String(20), nullable=False, default="Pending")
#     # Status will be one of these options: 'Pending', 'Accepted', 'Finished' and maybe 'Reviewed'? Don't know yet

class JobSchema(ModelSchema):
    class Meta:
        model = Job
        sql_session = db.session


class Transaction (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    code = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class TransactionSchema(ModelSchema):
    class Meta:
        model = Transaction
        sql_session = db.session

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # performer_id = db.Column(db.Integer, db.ForeignKey('performer.id', nullable=False))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    content = db.Column(db.String(200), nullable=False)

class ReportSchema(ModelSchema):
    class Meta:
        model = Report
        sql_session = db.session
