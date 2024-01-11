from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = SQLAlchemy()

class Product(db.Model):
    ID_product = db.Column(db.Integer, primary_key=True)
    img_product = db.Column(db.String(99), nullable=True, default='icons/alce.png')
    title_product = db.Column(db.String(80), nullable=False)
    description_product = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    #FK
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID_user'), nullable=False)
    user = db.relationship('User', backref=db.backref('products', lazy=True))

class User(db.Model, UserMixin):
    ID_user = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    user_lastname = db.Column(db.String(30), unique=True, nullable=False)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    user_phone = db.Column(db.String(10), unique=True, nullable=False)
    user_password = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return self.user_password == password  ####
    def get_id(self):
        return str(self.ID_user)

