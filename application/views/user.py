from flask import Blueprint, render_template, request, flash, redirect, url_for
from application import db   #means from __init__.py import db
from flask_login import login_required, logout_user, current_user
from application.models.user import User
from application.forms.user_form import UpdateUserForm
from application.services.user_service import UserService

user = Blueprint('user', __name__)

@user.route('/')
@login_required
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('user/users.html', users=users)


@user.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    form = UpdateUserForm()
    user = UserService.get_user_by_id(user_id)

    if user.id == current_user.id:
        flash('You are not authorized to your own details.', 'danger')
        return redirect(url_for('user.list_users'))

    return render_template('user/edit.html', user=user, form=form)



