from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager
from .forms import LoginForm, SignUpForm
from .models import users

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        print(">> Login button Clicked <<")
        if form.validate_on_submit():
            print(">> Login validate Clicked <<")
            username = request.form.get('username')
            password = request.form.get('password')

            # Check if user exists
            user = users.query.filter_by(username=username).first()
            print("User: ", user)
            if user is None:
                flash('Username is not valid.', category='danger')
            elif not check_password_hash(user.password, password):
                flash('Password is not valid.', category='danger')
            else:
                login_user(user)
                # Flash welcome message
                flash(f'Welcome back ! {user.username}', category='success')
                # Create session
                session['user'] = username
                session['is_logged_in'] = True
                session['is_authenticated'] = True
                return redirect(url_for('main.home'))

    return render_template('login.html', form=form)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    print("In signup")
    if request.method == 'POST':
        username = request.form.get('username')
        display_name = request.form.get('display_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Basic validation
        if users.query.filter_by(email=email).first():
            flash('Email is already registered.', category='danger')
        elif users.query.filter_by(username=username).first():
            flash('Username is already taken.', category='danger')
            print("Taken username ============")
        elif password != confirm_password:
            flash('Passwords do not match.', category='danger')
        else:
            # Create user
            hashed_password = generate_password_hash(password, method='scrypt',
                                                     salt_length=8)
            new_user = users(username=username.lower(), display_name=display_name, email=email,
                             password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash(message='Account created successfully!', category='success')
            return redirect(url_for('main.login'))

    return render_template('signup.html', title="Sign Up", form=SignUpForm())


@main.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('Logout successful!', category='success')
    return redirect(url_for('main.login'))
