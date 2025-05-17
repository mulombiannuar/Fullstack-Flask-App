from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from application.forms.user_form import RegistrationForm, UpdateUserForm, PasswordForm
from application.services.user_service import UserService
from werkzeug.security import check_password_hash

home = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
def home_page():
    form = RegistrationForm()
    return render_template('auth/login.html', form=form)


@home.route('/dashboard', methods=['GET'])
@login_required
def dashboard_page():
    return render_template('home/dashboard.html')


@home.route('/messages', methods=['GET'])
@login_required
def messages_page():
    return render_template('home/messages.html')


@home.route('/profile')
@login_required
def profile():
    form = UpdateUserForm()
    return render_template('user/profile.html', form=form, user=current_user)


@home.route('/profile', methods=['GET', 'POST'])
@login_required
def update_profile():
     form = UpdateUserForm()
     if form.validate_on_submit():  
        data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'address': form.address.data,
            'zip_code': form.zip_code.data,
            'gender': form.gender.data
        }
        profile_updated = UserService.update_user(current_user.id, data)
        if profile_updated:
            flash(message='Profile details updated successfully!', category='success')
            return redirect(url_for('home.profile'))
        else:
            flash(message='Profile details updation failed. Please try again.', category='danger')
            return redirect(url_for('home.profile'))
    
     return render_template('home/profile.html', form=form)



@home.route('/password')
@login_required
def change_password():
    form = PasswordForm()
    return render_template('user/password.html', form=form)



@home.route('/password', methods=['GET', 'POST'])
@login_required
def update_password():
     form = PasswordForm()
     if form.validate_on_submit():  
        
        new_password = form.password.data
        old_password = form.old_password.data
        current_password = current_user.password
        
        if check_password_hash(current_password, old_password):            
            password_updated = UserService.update_user_password(current_user.id, new_password)
            if password_updated:
                flash(message='Account password updated successfully!', category='success')
                return redirect(url_for('home.dashboard_page'))
            else:
                flash(message='Password updation failed. Please try again.', category='danger')
        else:
           flash(message='The password you have entered does not match the existing one.', category='danger')
     
     return render_template('user/password.html', form=form)
