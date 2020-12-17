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

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    performer_id = db.Column(db.Integer, db.ForeignKey('performer.id', nullable=False))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    sender = db.Column(db.String(10), nullable=False)
    content = db.Column(db.String(200), nullable=False)

class MessageSchema(ModelSchema):
    class Meta:
        model = Message
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

#
# from sqlathanor import declarative_base, Column, relationship
# from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, func
# BaseModel = declarative_base()

# class User(BaseModel):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True, supports_json = True)
#     email = Column(String(120), unique=True, nullable=False, supports_json = True)
#     password = Column(String(200), nullable=False, supports_json = True)
#     role = Column(String(20), nullable=False, supports_json = True)
#     performer = relationship('Performer', backref="user", lazy=True, uselist=False, supports_json=True)
#     customer = relationship('Customer', backref="user", lazy=True, uselist=False, supports_json = True)
#
#     def __init__(self,email,password,role):
#         self.email = email
#         self.password = password
#         self.role = role
#
#
# class Performer(BaseModel):
#     __tablename__ = 'performers'
#     id = Column(Integer, primary_key=True, supports_json=True)
#     # username = Column(String(50), unique=True, nullable=False)
#     email = Column(String(120), unique=True, nullable=False, supports_json=True)
#     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#     # user = relationship("User", back_populates="performer", supports_json=True)
#
#     name = Column(String(50), nullable=False, supports_json=True)
#     cost_per_hour = Column(Float, nullable=True, supports_json=True)
#     profile_pic_url = Column(String(100), nullable=True, supports_json=True)
#     birthday = Column(DateTime, nullable=True, supports_json=True)
#     score = Column(Float, nullable=False, default=0, supports_json=True)
#     search_city = Column(String(30), nullable=True, supports_json=True)
#     search_state = Column(String(30), nullable=True, supports_json=True)
#     fiscal_code = Column(String(20), nullable=True, supports_json=True)
#     money = Column(Float, nullable=False, default=0, supports_json=True)
#     created_at = Column(DateTime, server_default=func.now(), supports_json=True)
#     updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), supports_json=True)
#
#
# class Customer(BaseModel):
#     __tablename__ = 'customers'
#     id = Column(Integer, primary_key=True, supports_json=True)
#     # username = Column(String(50), unique=True, nullable=False)
#     email = Column(String(120), unique=True, nullable=False, supports_json=True)
#     # user = relationship("User", back_populates="performer", supports_json=True)
#     user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
#     name = Column(String(50), nullable=False, supports_json=True)
#     profile_pic_url = Column(String(50), nullable=True, supports_json=True)
#     birthday = Column(DateTime, nullable=False, supports_json=True)
#     score = Column(Float, nullable=False, default=0, supports_json=True)
#     fiscal_code = Column(String(20), nullable=True, supports_json=True)
#     created_at = Column(DateTime, server_default=func.now(), supports_json=True)
#     updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now(), supports_json=True)
