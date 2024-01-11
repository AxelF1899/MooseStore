#apartado bibliotecas
import os
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, abort
from models import Product, db, User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

# Instancia de la app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdff2fa391720157041525004332a11c'

# Inicialización del administrador de la sesión
login_manager = LoginManager(app)

#apartado rutas

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

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
                flash('Login successful!', 'info')
                return redirect(url_for('home'))
            else:
                flash('Login unsuccessful. Incorrect password.', 'danger')
        else:
            flash('Login unsuccessful. User does not exist.', 'danger')

    return render_template('login.html')


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

        new_user = User(user_name=user_name,
                        user_lastname = user_lastname,
                        user_phone = user_phone,
                        user_email=user_email,
                        user_password = user_password
                        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'info')
        #print('Mensajes Flash:', get_flashed_messages(with_categories=True))
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    if request.method == 'POST':
        product_img_path = 'C:/Users/pablo/PROJECTS/MooseStore/static/icons/alce.png'
        product_title = request.form.get('title')
        product_description = request.form.get('description')
        product_price = request.form.get('price')    
        
        if 'image' in request.files:
            product_image = request.files['image']
            
            
            filename = secure_filename(product_image.filename)
            product_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            
            product_img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        new_product = Product(
            title_product=product_title,
            description_product=product_description,
            price=product_price,
            img_product=product_img_path, 
            user_id=current_user.ID_user
        )

        db.session.add(new_product)
        db.session.commit()

        flash('Product successfully listed for sale!', 'success')
        return redirect(url_for('home'))

    return render_template('sell.html')


@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    if request.method == 'POST':
        
        product_id = request.form.get('product_id')

        

        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            flash('Compra realizada con éxito', 'success')
            return redirect(url_for('home'))
        else:
            abort(404)

        flash('Compra realizada con éxito', 'success')
        return redirect(url_for('home'))

    return render_template('buy.html')


#Run application
if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/moosestore'
    app.config['UPLOAD_FOLDER'] = 'C:/Users/pablo/PROJECTS/MooseStore/static/icons/imgs'
    db.init_app(app) 
    app.run(debug=True)
