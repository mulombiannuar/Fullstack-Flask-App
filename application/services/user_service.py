from application import db, mail
from application.models.user import User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app, url_for, render_template
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

class UserService:
    
    @staticmethod
    def get_all_users():
        try:
            return User.query.order_by(User.created_at.desc()).all()
        except SQLAlchemyError as e:
            print(f"Error geting users: {str(e)}")
            return None
    
    
    @staticmethod
    def create_user(data):
        try:
            hashed_password = generate_password_hash(data['password'])
            user = User(
                email=data['email'],
                password=hashed_password,
                first_name=data['first_name'],
                last_name=data['last_name'],
                gender=data['gender'],
                address=data.get('address', ''),
                zip_code=data.get('zip_code', '')
            )
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error creating user: {str(e)}")
            return None

   
    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            print(f"Error fetching user: {str(e)}")
            return None
        
        
    @staticmethod
    def get_user_by_email(email):
        try:
            return User.query.filter_by(email=email).first()  
        except SQLAlchemyError as e:
            print(f"Error fetching user: {str(e)}")
            return None

        
    @staticmethod
    def update_user(user_id, data):
        try:
            user = User.query.get(user_id)
            if not user:
                return None

            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)
            user.gender = data.get('gender', user.gender)
            user.address = data.get('address', user.address)
            user.zip_code = data.get('zip_code', user.zip_code)

            if 'password' in data and data['password']:
                user.password = generate_password_hash(data['password'])

            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating user: {str(e)}")
            return None


    @staticmethod
    def delete_user(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return False
            
            db.session.delete(user)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error deleting user: {str(e)}")
            return False
        
    
    @staticmethod
    def update_user_password(user_id, new_password):
        try:
            user = User.query.get(user_id)
            if not user:
                return False
            
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error updating user password: {str(e)}")
            return False
        
        
    @staticmethod   
    def generate_reset_token(email):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=current_app.config['PASSWORD_RESET_SALT'])
    
    
    
    @staticmethod
    def send_reset_email(email, token):
        reset_url = url_for('auth.reset_password_page', token=token, _external=True)
        subject = "Password Reset Request"
        msg = Message(subject, recipients=[email])

        # Fallback plain text version
        msg.body = f"""Hi,

        We received a request to reset your password.

        Click the link below to reset your password:
        {reset_url}

        If you didn’t make this request, just ignore this message.

        Thanks,
        Your Team
        """

        # HTML version
        msg.html = render_template('email/reset_password.html', reset_url=reset_url)

        mail.send(msg)
