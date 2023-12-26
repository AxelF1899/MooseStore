from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

class User(db.Model, UserMixin):
    ID_user = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30), unique=True, nullable=False)
    user_lastname = db.Column(db.String(30), unique=True, nullable=False)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    user_phone = db.Column(db.String(10), unique=True, nullable=False)
    user_password = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)
