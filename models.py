from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    performer_id = db.relationship('Performer', backref='User', lazy=True,uselist=False)
    customer_id = db.relationship('Customer', backref='User', lazy=True,uselist=False)


class Performer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
    name = db.Column(db.String(50), nullable=False)
    profile_pic_url = db.Column(db.String(50), nullable=True)
    birthday = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Float, nullable=False, default=0)
    fiscal_code = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())