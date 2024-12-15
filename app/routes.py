import os

from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from . import db, login_manager
from .forms import LoginForm, ProfileForm, SignUpForm
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
                # Create session
                session['user'] = username
                session['is_logged_in'] = True
                session['is_authenticated'] = True
                # Flash welcome message
                flash(f'Welcome back ! {
                      user.display_name}', category='success')
                return redirect(url_for('main.home'))

    return render_template('login.html', form=form)


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()  # Create an instance of the SignUpForm

    if form.validate_on_submit():  # Check if the form is submitted and valid
        username = form.username.data
        display_name = form.display_name.data
        email = form.email.data
        password = form.password.data

        # Basic validation
        if users.query.filter_by(email=email).first():
            flash('Email is already registered.', category='danger')
        elif users.query.filter_by(username=username).first():
            flash('Username is already taken.', category='danger')
        else:
            # Create user
            hashed_password = generate_password_hash(
                password, method='scrypt', salt_length=8)
            new_user = users(username=username.lower(
            ), display_name=display_name, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash(message='Account created successfully!', category='success')
            return redirect(url_for('main.login'))

    return render_template('signup.html', title="Sign Up", form=form)


@main.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('Logout successful!', category='success')
    return redirect(url_for('main.login'))


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    user = current_user

    if request.method == 'POST':
        # Update user attributes
        user.username = form.username.data
        user.display_name = form.display_name.data
        user.email = form.email.data
        user.bio = form.bio.data

        # Handle profile picture upload
        if form.avatar.data:
            avatar_file = form.avatar.data
            avatar_filename = secure_filename(avatar_file.filename)

            # Check file size
            # Move cursor to the end of the file
            avatar_file.seek(0, os.SEEK_END)
            file_size = avatar_file.tell()    # Get file size in bytes
            avatar_file.seek(0)              # Reset file pointer to the start

            # 2MB limit (2 * 1024 * 1024 bytes)
            if file_size > 2 * 1024 * 1024:
                flash('File size must be less than or equal to 2MB.',
                      category='error')
                return redirect(url_for('main.profile'))

            # Save the file
            avatar_file.save(os.path.join(current_app.root_path,
                             'static/profile_pics', avatar_filename))
            user.image_file = avatar_filename

        db.session.commit()
        flash('Profile updated successfully!', category='success')
        return redirect(url_for('main.profile'))

    # Pre-fill form with current user data
    form.avatar.data = user.image_file
    form.username.data = user.username
    form.display_name.data = user.display_name
    form.email.data = user.email
    form.bio.data = user.bio
    return render_template('profile.html', form=form, user=user)
