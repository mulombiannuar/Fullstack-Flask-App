from flask import Blueprint, render_template, request, flash, redirect, url_for
from application import db   #means from __init__.py import db
from flask_login import login_required, logout_user, current_user
from application.forms.user_form import UpdateUserForm, DeleteUserForm
from application.services.user_service import UserService

user = Blueprint('user', __name__)

@user.route('/')
@login_required
def list_users():
    form = DeleteUserForm()
    users = UserService.get_all_users()
    return render_template('user/users.html', users=users, form=form)


@user.route('/<int:user_id>')
@login_required
def show_user(user_id):
    user = UserService.get_user_by_id(user_id)
    return render_template('user/show.html', user=user)


@user.route('/<int:user_id>/edit')
@login_required
def edit_user(user_id):
    form = UpdateUserForm()
    user = UserService.get_user_by_id(user_id)
    
    return render_template('user/edit.html', user=user, form=form)


@user.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    form = UpdateUserForm()
    user = UserService.get_user_by_id(user_id)
    
    if request.method == 'POST' and form.validate_on_submit():  
        data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data,
            'address': form.address.data,
            'zip_code': form.zip_code.data,
            'gender': form.gender.data
        }
        user_updated = UserService.update_user(user_id, data)
        if user_updated:
            flash(message='User details updated successfully!', category='success')
            return redirect(url_for('user.list_users'))
        else:
            flash(message='User details updation failed. Please try again.', category='danger')
            return redirect(url_for('user.list_users'))
    
    return render_template('user/edit.html', user=user, form=form)



@user.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = UserService.get_user_by_id(user_id)

    if user.id == current_user.id:
        flash('You are not authorized to delete your own details.', 'danger')
        return redirect(url_for('user.list_users'))

    user_deleted = UserService.delete_user(user_id)
    if user_deleted:
        flash('User deleted successfully!', 'success')
        return redirect(url_for('user.list_users'))
    else:
        flash('There was a problem while deleting user. Please try again!', 'danger')
        return redirect(url_for('user.list_users'))


