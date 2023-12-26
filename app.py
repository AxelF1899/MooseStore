#apartado bibliotecas
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from models import Product, db, User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Instancia de la app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdff2fa391720157041525004332a11c'

# Inicialización de LoginManager
login_manager = LoginManager(app)

#apartado rutas

@app.route('/')
def home():
    return render_template('home.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')
        user = User.query.filter_by(user_email=user_email).first()

        if user:
            if user.check_password(user_password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login unsuccessful. Incorrect password.', 'danger')
        else:
            flash('Login unsuccessful. User does not exist.', 'danger')

    return render_template('home.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('firstName')
        user_lastname = request.form.get('lastName')
        user_email = request.form.get('email')
        user_phone = request.form.get('phone')  
        user_password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        if user_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('register'))
        
        existing_user = User.query.filter_by(user_email=user_email).first()  
        if existing_user:
            flash('An account with this email already exists. Please log in or use a different email.', 'danger')
            return redirect(url_for('register'))

        # Crea un nuevo usuario
        new_user = User(user_name=user_name,
                        user_lastname = user_lastname,
                        user_phone = user_phone,
                        user_email=user_email,
                        user_password = user_password
                        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        print('Mensajes Flash:', get_flashed_messages(with_categories=True))
        return redirect(url_for('login'))

    return render_template('login.html')


#Run application
if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/moosestore'
    db.init_app(app) 
    app.run(debug=True)
