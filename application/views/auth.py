from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash
from application.services.user_service import UserService
from application.forms.auth_form import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from application import mail

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET'])
def login_page():
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth.route('/login', methods=['POST'])
def login_handler():
    form = LoginForm()  
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember.data  

        user = UserService.get_user_by_email(email)
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=remember_me)
                return redirect(url_for('home.dashboard_page'))
            else:
                flash('Incorrect password, try again.', category='danger') 
        else:
            flash('Email address does not exist.', category='danger') 
            
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET'])
def register_page():
    form = RegistrationForm()
    return render_template('auth/register.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():  
        data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'password': form.password.data,
            'address': form.address.data,
            'zip_code': form.zip_code.data,
            'gender': form.gender.data
        }
        user = UserService.create_user(data)
        if user:
            flash(message='Your registration was successful. Please proceed to login!', category='success')
            return redirect(url_for('auth.login_page'))
        else:
            flash(message='Registration failed. Please try again.', category='danger')
            return redirect(url_for('auth.register_page'))
    
    return render_template('auth/register.html', form=form)
    

@auth.route('/forgot-password', methods=['GET'])
def forgot_password_page():
    form = RegistrationForm()
    return render_template('auth/forgot_password.html', form=form)


@auth.route('/forgot-password', methods=['POST'])
def send_password_reset_link():
    form = ForgotPasswordForm()  

    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        user = UserService.get_user_by_email(email)

        if user:
            try:
                token = UserService.generate_reset_token(user.email)
                UserService.send_reset_email(user.email, token)
                flash('A password reset link has been sent to your email.', category='success')
                return redirect(url_for('auth.login_page'))
            except Exception as e:
                current_app.logger.error(f"Error sending reset email: {str(e)}")
                flash('An error occurred. Please try again later.', category='danger')
        else:
            flash('No account found with that email. Please try again.', category='warning')

    return render_template('auth/forgot_password.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET'])
def reset_password_page(token):
    form = ResetPasswordForm()
    return render_template('auth/reset_password.html', token=token, form=form)


@auth.route('/reset-password/<token>', methods=['POST'])
def reset_user_password(token):
    
    form = ResetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        password = form.password.data

        try:
            serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
            email = serializer.loads(
                token,
                salt=current_app.config['PASSWORD_RESET_SALT'],
                max_age=3600  # 1 hour expiry
            )
        except SignatureExpired:
            flash("The password reset link has expired.", category="warning")
            return redirect(url_for('auth.forgot_password_page'))
        except BadSignature:
            flash("Invalid or corrupted token.", category="danger")
            return redirect(url_for('auth.forgot_password_page'))

        user = UserService.get_user_by_email(email)
        if user:
            UserService.update_user_password(user.id, password)
            flash("Your password has been updated successfully.", category="success")
            return redirect(url_for('auth.login_page'))
        else:
            flash("No account found for this reset link.", category="danger")
            return redirect(url_for('auth.forgot_password_page'))

    return render_template('auth/reset_password.html', form=form, token=token)


@auth.route('/logout')
@login_required
def logout_handler():
    logout_user()
    flash('You are logged out successfully!', category='success')
    return redirect(url_for('auth.login_page'))