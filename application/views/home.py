from flask import Blueprint, render_template
from flask_login import login_required, current_user
from application.forms.user_form import RegistrationForm

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
    return render_template('user/users.html', user=current_user)


@home.route('/profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    pass


@home.route('/password')
@login_required
def change_password():
    pass


@home.route('/password', methods=['GET', 'POST'])
@login_required
def update_password():
    pass