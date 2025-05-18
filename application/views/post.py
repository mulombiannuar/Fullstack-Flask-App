from flask import Blueprint, render_template, request, redirect, url_for, flash,current_app
from flask_login import login_required, current_user
from application.models.post import Post
from application.services.post_service import PostService
from application.forms.post_form import PostForm, DeletePostForm
from application import db
import os
from werkzeug.utils import secure_filename

post = Blueprint('post', __name__)

@post.route('/')
@login_required
def list_posts():
    form = DeletePostForm()
    posts = PostService.get_all_posts()
    return render_template('post/posts.html', posts=posts, form=form)



@post.route('/create')
@login_required
def create_post():
    form = PostForm()
    return render_template('post/create_post.html', form=form)



@post.route('/create', methods=['GET', 'POST'])
@login_required
def save_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        post_image = request.files.get('post_image')
        filename = 'default.jpg'
        if post_image and post_image.filename != '':
            filename = secure_filename(post_image.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            post_image.save(upload_path)

        data = {
            'title': form.title.data,
            'content': form.content.data,
            'post_image': form.post_image.data
        }
        
        post_created = PostService.create_post(data)
        if post_created:
            flash(message='Post created successfully!', category='success')
            return redirect(url_for('post.list_posts'))
        else:
            flash(message='Post could not be created!', category='danger')
    
    return render_template('post/create_post.html', form=form)




@post.route('/<int:post_id>/edit')
@login_required
def edit_post(post_id):
    post = PostService.get_post_by_id(post_id)
    
    if not post:
        flash('Post not found!', 'danger')
        return redirect(url_for('post.list_posts'))

    if post.user_id != current_user.id:
        flash('You are not authorized to edit this post.', 'error')
        return redirect(url_for('post.list_posts'))

    return render_template('post/edit_post.html', post=post)



@post.route('/<int:post_id>/edit')
@login_required
def update_post(post_id):
    form = PostForm()
    post = PostService.get_post_by_id(post_id)

    if request.method == 'POST' and form.validate_on_submit():
        
        post_image = request.files.get('post_image')
        
        if post_image and post_image.filename != '':
            # delete old image if exists
            if post.post_image:
                old_image_path = os.path.join(current_app.root_path, 'static/uploads', post.post_image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # save new image
            filename = secure_filename(post_image.filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            post_image.save(upload_path)
        else:
            filename = post.post_image  

        data = {
            'title': form.title.data,
            'content': form.content.data,
            'post_image': filename
        }
        
        post_updated = PostService.update_post(post_id, data)
        if post_updated:
            flash(message='Post updated successfully!', category='success')
            return redirect(url_for('post.list_posts'))
        else:
            flash(message='Post could not be updated!', category='danger')
    
    return render_template('post/edit_post.html', post=post)



@post.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = PostService.get_post_by_id(post_id)
    if not post:
        flash('Post not found!', 'danger')
        return redirect(url_for('post.list_posts'))

    # delete post image file if exists
    if post.post_image:
        image_path = os.path.join(current_app.root_path, 'static/uploads', post.post_image)
        if os.path.exists(image_path):
            os.remove(image_path)

    post_deleted = PostService.delete_post(post_id)
    if post_deleted:
        flash('Post deleted successfully!', 'success')
    else:
        flash('Post could not be deleted!', 'danger')
    return redirect(url_for('post.list_posts'))
