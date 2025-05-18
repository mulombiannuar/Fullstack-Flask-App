from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class PostForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(message="Title is required."),
        Length(min=5, max=200, message="Title must be between 5 and 200 characters.")
    ])
    
    post_image = FileField('Post Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], message="Only image files are allowed.")
    ])

    content = TextAreaField('Content', validators=[
        DataRequired(message="Content is required."),
        Length(min=10, message="Content must be at least 10 characters long.")
    ])
    
    
class DeletePostForm(FlaskForm):
    """A form for CSRF-protected delete actions."""
    pass 
