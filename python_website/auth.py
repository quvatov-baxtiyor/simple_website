from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from . import db
from .models import User
from werkzeug import generate_password_hash,check_password_hash
from flask_login import login_user,login_required, logout_user,current_user



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wrong',category='error')
        else:
            flash('Invalid',category='error')
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered!',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters',category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 characters',category='error')
        elif password1 != password2:
            flash('Passwords do not match',category = 'error')
        elif len(password1) < 7:
            flash('Password is too short',category = 'error')
        else:
            new_user = User(email = email,firstname = firstname,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            #add user to database
            flash('Account created',category = 'success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user = current_user)

