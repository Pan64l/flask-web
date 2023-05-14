from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . models import User
from. import database
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email = email).first()
    
    if email == None:
        flash('Please enter an email', category='error') ##change a category
    elif user:
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Successfully logged in', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Incorrect password', category='error')
    elif user is None:
        flash('User not found', category='error')
        
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods= ['GET', 'POST'])
def sign_up():
    
    if request.method == 'POST':
        email = request.form['email']
        first_Name = request.form['firstName']
        password1 = request.form['password1']
        password2 = request.form['password2']
        
        user = User.query.filter_by(email = email).first()
        
        if user:
            flash('User already exists', category='error')       
        elif len(email) < 5:
            flash('Email must be at least 5 characters', category='error')
        elif len(first_Name) < 2:
            flash('First name must be greater than 1 characters', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters', category='error')
        elif password1!= password2:
            flash('Passwords do not match', category= 'error')
        else:
            new_user = User(email = email ,first_name = first_Name, password = generate_password_hash(password1, method = 'sha256'))
            database.session.add(new_user)
            database.session.commit()
            login_user(user, remember=True)
            flash('Successfully signed up', category = 'success')
            return redirect(url_for('login.html'))
            #could be redirect('/')
            # we need to add the user information to the database
        
    return render_template("sign_up.html", user = current_user)

# @auth.route('/')
# def home():
#     return render_template("home.html")



