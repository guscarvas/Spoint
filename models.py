from app import db, ma
from marshmallow_sqlalchemy import ModelSchema


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    performer = db.relationship('Performer', lazy=True, uselist=False, back_populates="user")
    customer = db.relationship('Customer', lazy=True, uselist=False, back_populates="user")

    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role


class Performer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="performer")
    name = db.Column(db.String(50), nullable=False)
    cost_per_hour = db.Column(db.Float, nullable=True)
    profile_pic_url = db.Column(db.String(100), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)
    score = db.Column(db.Float, nullable=False, default=0)
    search_city = db.Column(db.String(30), nullable=True)
    search_state = db.Column(db.String(30), nullable=True)
    fiscal_code = db.Column(db.String(20), nullable=True)
    money = db.Column(db.Float, nullable=False, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="customer")
    name = db.Column(db.String(50), nullable=False)
    profile_pic_url = db.Column(db.String(50), nullable=True)
    birthday = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Float, nullable=False, default=0)
    fiscal_code = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


class UserSchema(ModelSchema):
    class Meta:
        model = User
        sql_session = db.session


class PerformerSchema(ModelSchema):
    class Meta:
        model = Performer
        sql_session = db.session


class CustomerSchema(ModelSchema):
    class Meta:
        model = Customer
        sql_session = db.session


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #customer_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False )
    performer_id = db.Column(db.Integer, db.ForeignKey('performer.id'))
    hours_booked = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    performer_score = db.Column(db.Float, nullable=False, default=0)
    date = db.Column(db.DateTime, nullable=False)
    # customer_score =
    # status =
    price_per_hour = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


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
