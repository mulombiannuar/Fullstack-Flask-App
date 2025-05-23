from flask_wtf import FlaskForm
from wtforms.validators import Email
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

    
class UpdateUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(message="First name is required."),
        Length(min=2, max=150, message="First name must be between 2 and 150 characters.")
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message="Last name is required."),
        Length(min=2, max=150, message="Last name must be between 2 and 150 characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email address is required."),
        Email(message="Please enter a valid email address.")
    ])
    address = StringField('Address', validators=[
        DataRequired(message="Address is required."),
        Length(min=10, max=255, message="Address must be between 10 and 255 characters.")
    ])
    zip_code = StringField('Zip Code', validators=[
        DataRequired(message="Zip code is required."),
        Length(min=5, max=20, message="Zip code must be between 5 and 20 characters.")
    ])
    gender = StringField('Gender', validators=[
        DataRequired(message="Please select your gender.")
    ])
    

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=8, message="Password must be at least 8 characters long.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    old_password = PasswordField('Old Password', validators=[
        DataRequired(message="Old Password is required.")
    ])
    
    
class DeleteUserForm(FlaskForm):
    """A form for CSRF-protected delete actions."""
    pass 


