from flask import Blueprint, render_template, request, flash, redirect, url_for
from application import db   #means from __init__.py import db
from flask_login import login_required, logout_user, current_user
from application.models.user import User

user = Blueprint('user', __name__)

@user.route('/')
@login_required
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('user/users.html', users=users)






